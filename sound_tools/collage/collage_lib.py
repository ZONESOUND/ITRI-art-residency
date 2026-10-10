"""
collage_lib.py：《節奏繞纏》第四幕旅行拼貼三個 agent 共用的工具。
所有素材統一 48 kHz 立體聲 float64，內部電平以 LUFS 為準。

重點 API
  load(path)                    -> (N,2) 48k
  lufs(x) / norm_lufs(x, t)     整段響度量測與正規化（pyloudnorm）
  leveler(x, win_s, max_gain_db) 慢速電平器：把 win_s 尺度的起伏壓平（實現「音壓一致」的核心）
  fade(x, in_s, out_s)、xfade_concat([...], xf_s)  等功率交叉淡化串接
  place(bus, seg, t, gain_db, pan)  疊到時間軸
  reverb(x, rt60, lp_hz, predelay_ms, mix)、delay(x, time_s, fb, lp_hz, mix)
  lowpass/highpass/bandpass、pitch_shift_semitones（varispeed）、reverse
  phrases(mono, top_db)          能量分段（朗讀單詞用）
  finalize(x, target_lufs, tp_db) 最後鏈：leveler → 軟壓縮 → 限幅 → 正規化到目標響度
  write(path, x) + measure(path) 寫 24-bit wav 與 mp3，並用 ffmpeg ebur128 量 I / LRA / TP / 短期起伏
"""
import os, math, subprocess, json, re
import numpy as np
import soundfile as sf
import pyloudnorm as pyln
from scipy.signal import resample_poly, butter, sosfiltfilt, fftconvolve, lfilter

SR = 48000
_METER = pyln.Meter(SR)

ROOT = os.path.expanduser("~/Library/Mobile Documents/com~apple~CloudDocs/Documents/03_Projects_Operations/Active/ITRI_工研院藝術進駐/錄音")
TRAVEL = os.path.join(ROOT, "旅行移動素材")

# ------------------------------------------------------------------ I/O
def load(path, sr=SR):
    """讀任何 wav/aif/mp3，轉 48k 立體聲 float64。mp3 走 ffmpeg。"""
    if not os.path.isabs(path):
        path = os.path.join(ROOT, path)
    if path.lower().endswith(".mp3"):
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "2", "-ar", str(sr), "-"],
                             capture_output=True, check=True).stdout
        return np.frombuffer(raw, dtype=np.float32).reshape(-1, 2).astype(np.float64)
    y, s = sf.read(path, always_2d=True)
    y = y.astype(np.float64)
    if y.shape[1] == 1:
        y = np.repeat(y, 2, axis=1)
    elif y.shape[1] > 2:
        y = y[:, :2]
    if s != sr:
        g = math.gcd(sr, s)
        y = resample_poly(y, sr // g, s // g, axis=0)
    return y

def mono(x):
    return x.mean(axis=1) if x.ndim == 2 else x

def stereo(x):
    return np.stack([x, x], axis=1) if x.ndim == 1 else x

def write(path, x, mp3=True):
    """48k 24-bit wav；mp3=True 另存 192k mp3 給試聽。"""
    x = stereo(np.asarray(x, dtype=np.float64))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    sf.write(path, np.clip(x, -1, 1), SR, subtype="PCM_24")
    if mp3:
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", path, "-codec:a", "libmp3lame", "-b:a", "192k",
                        os.path.splitext(path)[0] + ".mp3"], check=True)
    return path

# ------------------------------------------------------------------ 響度
def lufs(x):
    x = stereo(x)
    if len(x) < SR * 0.4:
        return -70.0
    v = _METER.integrated_loudness(x)
    return -70.0 if not np.isfinite(v) else float(v)

def norm_lufs(x, target=-20.0):
    cur = lufs(x)
    if cur <= -69:
        return x
    return x * 10 ** ((target - cur) / 20)

def db(g):
    return 10 ** (g / 20)

def rms_db(x):
    return 20 * math.log10(np.sqrt(np.mean(stereo(x) ** 2)) + 1e-12)

def k_weight(m):
    """ITU-R BS.1770 的 K 加權（高架 + 高通），用 pyloudnorm 的係數。給電平器旁鏈用。"""
    for f in _METER._filters.values():
        m = lfilter(f.b, f.a, m)
    return m

def leveler(x, win_s=2.0, max_gain_db=12.0, target_rms_db=None, floor_db=-60.0):
    """慢速電平器。用 win_s 秒、K 加權的 RMS 包絡算增益，把起伏拉平到 target。
    增益上下限 ±max_gain_db；低於 floor_db 的地方（真靜音）不拉。
    這是「讓握的人感覺力氣一樣」的核心手段，把它視為一個很慢的 AGC。"""
    x = stereo(x)
    m = k_weight(mono(x))
    n = len(m)
    hop = int(SR * 0.05)
    win = int(SR * win_s)
    env = np.zeros(n // hop + 1)
    sq = m ** 2
    cs = np.concatenate([[0], np.cumsum(sq)])
    for k in range(len(env)):
        c = k * hop
        a, b = max(0, c - win // 2), min(n, c + win // 2)
        env[k] = math.sqrt((cs[b] - cs[a]) / max(1, b - a) + 1e-12)
    env_db = 20 * np.log10(env + 1e-9)
    if target_rms_db is None:
        target_rms_db = float(np.median(env_db[env_db > floor_db])) if np.any(env_db > floor_db) else -20
    gain_db = np.clip(target_rms_db - env_db, -max_gain_db, max_gain_db)
    gain_db[env_db < floor_db] = 0.0
    # 平滑增益（約 win_s 的時間常數），避免抽吸
    alpha = math.exp(-1 / (win_s / 0.05 * 0.5))
    g = np.zeros_like(gain_db); acc = gain_db[0]
    for k in range(len(gain_db)):
        acc = alpha * acc + (1 - alpha) * gain_db[k]; g[k] = acc
    gain = np.interp(np.arange(n), np.arange(len(g)) * hop, db(g))
    return x * gain[:, None]

# ------------------------------------------------------------------ 淡化與拼接
def fade(x, in_s=0.01, out_s=0.01, shape="equal_power"):
    x = stereo(x).copy()
    n = len(x)
    fi, fo = int(in_s * SR), int(out_s * SR)
    fi, fo = min(fi, n), min(fo, n)
    if fi > 0:
        r = np.linspace(0, 1, fi)
        x[:fi] *= (np.sin(r * math.pi / 2) if shape == "equal_power" else r)[:, None]
    if fo > 0:
        r = np.linspace(1, 0, fo)
        x[n - fo:] *= (np.sin(r * math.pi / 2) if shape == "equal_power" else r)[:, None]
    return x

def xfade_concat(segs, xf_s=3.0):
    """等功率交叉淡化串接。xf_s 可以是單一值或每個接縫一個的 list。"""
    segs = [stereo(s) for s in segs]
    if isinstance(xf_s, (int, float)):
        xf_s = [xf_s] * (len(segs) - 1)
    out = segs[0].copy()
    for s, xf in zip(segs[1:], xf_s):
        n = int(min(xf * SR, len(out), len(s)))
        if n <= 0:
            out = np.concatenate([out, s]); continue
        r = np.linspace(0, 1, n)
        a, b = np.cos(r * math.pi / 2)[:, None], np.sin(r * math.pi / 2)[:, None]
        mid = out[-n:] * a + s[:n] * b
        out = np.concatenate([out[:-n], mid, s[n:]])
    return out

def loop_to(x, dur_s, xf_s=2.0):
    """把素材循環到 dur_s 秒，接縫用交叉淡化。"""
    x = stereo(x)
    need = int(dur_s * SR)
    if len(x) >= need:
        return x[:need]
    pieces = [x] * (need // max(1, len(x) - int(xf_s * SR)) + 2)
    return xfade_concat(pieces, xf_s)[:need]

def place(bus, seg, t, gain_db=0.0, pan=0.0):
    """把 seg 疊到 bus 的 t 秒處。pan -1..1 等功率。超出尾端自動截。"""
    seg = stereo(seg)
    n0 = int(t * SR)
    if n0 >= len(bus) or n0 + len(seg) <= 0:
        return
    if n0 < 0:
        seg = seg[-n0:]; n0 = 0
    seg = seg[:len(bus) - n0]
    th = (pan + 1) / 2 * math.pi / 2
    g = db(gain_db)
    bus[n0:n0 + len(seg), 0] += seg[:, 0] * math.cos(th) * math.sqrt(2) * g
    bus[n0:n0 + len(seg), 1] += seg[:, 1] * math.sin(th) * math.sqrt(2) * g

def timeline(dur_s):
    return np.zeros((int(dur_s * SR), 2))

# ------------------------------------------------------------------ 濾波與效果
def _sos(kind, hz, order=2):
    return butter(order, np.asarray(hz) / (SR / 2), btype=kind, output="sos")

def lowpass(x, hz, order=2):
    return sosfiltfilt(_sos("low", hz, order), stereo(x), axis=0)

def highpass(x, hz, order=2):
    return sosfiltfilt(_sos("high", hz, order), stereo(x), axis=0)

def bandpass(x, lo, hi, order=2):
    return sosfiltfilt(_sos("band", [lo, hi], order), stereo(x), axis=0)

def _ir(rt60, lp_hz, seed, predelay_ms):
    r = np.random.default_rng(seed)
    n = int(rt60 * 1.2 * SR)
    t = np.arange(n) / SR
    ir = np.stack([r.standard_normal(n), r.standard_normal(n)], axis=1) * (10 ** (-3 * t / rt60))[:, None]
    ir = lowpass(ir, lp_hz, 1)
    ir[:int(0.004 * SR)] *= 0.15
    pre = np.zeros((int(predelay_ms / 1000 * SR), 2))
    ir = np.concatenate([pre, ir])
    return ir / np.sqrt((ir ** 2).sum(axis=0)).max()

_IR_CACHE = {}
def reverb(x, rt60=2.5, lp_hz=4000, predelay_ms=20, mix=0.3, seed=1):
    """合成殘響（衰減雜訊 IR）。mix=0 全乾、1 全濕。回傳長度 = 原長 + 尾巴。"""
    key = (rt60, lp_hz, seed, predelay_ms)
    if key not in _IR_CACHE:
        _IR_CACHE[key] = _ir(rt60, lp_hz, seed, predelay_ms)
    ir = _IR_CACHE[key]
    x = stereo(x)
    wet = np.stack([fftconvolve(x[:, 0], ir[:, 0]), fftconvolve(x[:, 1], ir[:, 1])], axis=1)
    wet *= np.sqrt(np.mean(x ** 2)) / (np.sqrt(np.mean(wet ** 2)) + 1e-9)
    dry = np.concatenate([x, np.zeros((len(wet) - len(x), 2))])
    return dry * (1 - mix) + wet * mix

def delay(x, time_s=0.375, fb=0.4, lp_hz=3000, mix=0.3, taps=8, pingpong=False):
    x = stereo(x)
    d = int(time_s * SR)
    out = np.zeros((len(x) + taps * d, 2))
    out[:len(x)] += x * (1 - mix)
    cur = x.copy()
    for k in range(1, taps + 1):
        cur = lowpass(cur, lp_hz, 1) * fb
        if pingpong and k % 2:
            cur = cur[:, ::-1]
        out[k * d:k * d + len(cur)] += cur * mix
    return out

def reverse(x):
    return stereo(x)[::-1].copy()

def varispeed(x, semitones):
    """磁帶式變速：音高與速度一起變。"""
    x = stereo(x)
    rate = 2 ** (semitones / 12)
    pos = np.arange(int(len(x) / rate)) * rate
    i = np.clip(np.floor(pos).astype(int), 0, len(x) - 2)
    f = (pos - i)[:, None]
    return x[i] * (1 - f) + x[i + 1] * f

pitch_shift_semitones = varispeed

def saturate(x, drive=1.3):
    return np.tanh(drive * stereo(x)) / math.tanh(drive)

def phrases(m, top_db=30, min_len=0.4, gap=0.35, pad=0.06):
    """能量分段：回傳 [(start_s, end_s), ...]。給朗讀檔切單詞用。"""
    m = mono(m)
    hop = int(SR * 0.01)
    frames = np.lib.stride_tricks.sliding_window_view(m, 2048)[::hop]
    e = 20 * np.log10(np.sqrt(np.mean(frames ** 2, axis=1)) + 1e-9)
    on = e > (e.max() - top_db)
    iv = []
    k = 0
    while k < len(on):
        if on[k]:
            j = k
            while j < len(on) and on[j]:
                j += 1
            iv.append([k * hop / SR, (j * hop + 2048) / SR]); k = j
        else:
            k += 1
    ph = []
    for s, e_ in iv:
        if ph and s - ph[-1][1] < gap:
            ph[-1][1] = e_
        else:
            ph.append([s, e_])
    return [(max(0, s - pad), min(len(m) / SR, e_ + pad)) for s, e_ in ph if e_ - s >= min_len]

def cut(x, start_s, end_s=None, dur_s=None):
    x = stereo(x)
    a = int(start_s * SR)
    b = int((end_s if end_s is not None else start_s + dur_s) * SR)
    return x[a:b].copy()

# ------------------------------------------------------------------ 最後鏈與量測
def _compress(x, thresh_db=-18, ratio=3.0, attack_s=0.03, release_s=0.4):
    x = stereo(x)
    m = np.abs(mono(x))
    aa, ar = math.exp(-1 / (attack_s * SR)), math.exp(-1 / (release_s * SR))
    env = np.zeros(len(m)); acc = 0.0
    # 向量化近似：先用 lfilter 做 release 平滑，再取 attack 的快速跟隨
    env = lfilter([1 - ar], [1, -ar], m)
    env = np.maximum(env, lfilter([1 - aa], [1, -aa], m))
    env_db = 20 * np.log10(env + 1e-9)
    over = np.maximum(0, env_db - thresh_db)
    gain_db = -over * (1 - 1 / ratio)
    return x * db(gain_db)[:, None]

def _limiter(x, ceiling_db=-3.0, lookahead_s=0.005, release_s=0.1):
    x = stereo(x)
    c = db(ceiling_db)
    peak = np.max(np.abs(x), axis=1)
    la = int(lookahead_s * SR)
    # 前瞻：把峰值往前推
    pk = np.maximum.reduce([np.pad(peak, (0, k))[k:] for k in range(0, la, max(1, la // 8))] + [peak])
    need = np.minimum(1.0, c / (pk + 1e-9))
    ar = math.exp(-1 / (release_s * SR))
    g = np.ones(len(need)); acc = 1.0
    # 增益只能瞬間下降、慢慢回升
    for k in range(len(need)):
        acc = need[k] if need[k] < acc else ar * acc + (1 - ar) * need[k]
        g[k] = acc
    return x * g[:, None]

def finalize(x, target_lufs=-20.0, tp_db=-3.0, level_win_s=3.0, level_max_db=16.0, comp=True, edge_fade_s=1.0,
             fine_win_s=1.0, fine_max_db=6.0, comp_thresh_db=-20, comp_ratio=2.5):
    """最後鏈：慢速電平器（3 s 粗、再 1 s 細）→ 軟壓縮 → 正規化 → 限幅 → 再校正響度 → 頭尾 1 s 短淡化。
    目標：I ≈ target、LRA ≤ 3 LU、TP ≤ tp_db、3 秒短期響度相對 I 在 ±4 LU 內（頭尾 5 秒除外）。"""
    y = leveler(x, level_win_s, level_max_db)
    y = leveler(y, fine_win_s, fine_max_db)
    if comp:
        y = _compress(y, thresh_db=comp_thresh_db, ratio=comp_ratio)
    y = norm_lufs(y, target_lufs)
    y = _limiter(y, tp_db)
    y = norm_lufs(y, target_lufs)
    y = _limiter(y, tp_db)
    return fade(y, edge_fade_s, edge_fade_s)

def measure(path):
    """用 ffmpeg ebur128 量：I、LRA、TP，加上 3 秒短期響度的 p5/p95（相對 I）。"""
    p = subprocess.run(["ffmpeg", "-nostats", "-v", "info", "-i", path, "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    I = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", p)[-1])
    LRA = float(re.findall(r"LRA:\s+([\d.]+) LU", p)[-1])
    TP = max(float(v) for v in re.findall(r"Peak:\s+(-?[\d.]+) dBFS", p)[-2:])
    S = np.array([float(v) for v in re.findall(r"\sS:\s*(-?[\d.]+)", p)])
    S = S[np.isfinite(S) & (S > -60)]
    S = S[50:-50] if len(S) > 120 else S  # ebur128 每 0.1 s 一筆：略過頭尾 5 秒（淡入淡出與積分未穩定）
    rep = dict(I=I, LRA=LRA, TP=TP, S_p5_rel=float(np.percentile(S, 5) - I) if len(S) else None,
               S_p95_rel=float(np.percentile(S, 95) - I) if len(S) else None,
               S_min_rel=float(S.min() - I) if len(S) else None, S_max_rel=float(S.max() - I) if len(S) else None)
    return rep

def check(rep, target=-20.0, lra_max=3.0, tp_max=-3.0, s_dev=4.0):
    ok = abs(rep["I"] - target) <= 0.7 and rep["LRA"] <= lra_max and rep["TP"] <= tp_max + 0.1 \
         and rep["S_p5_rel"] is not None and rep["S_p5_rel"] >= -s_dev and rep["S_p95_rel"] <= s_dev
    return ok

def spectral_summary(x, n=8192):
    """粗略頻譜：質心與四個頻帶的相對能量（dB），拿來跟參考檔比質地。"""
    m = mono(x)
    m = m[: (len(m) // n) * n].reshape(-1, n)
    m = m[:: max(1, len(m) // 400)]
    spec = np.mean(np.abs(np.fft.rfft(m * np.hanning(n), axis=1)) ** 2, axis=0)
    f = np.fft.rfftfreq(n, 1 / SR)
    cent = float((spec * f).sum() / spec.sum())
    bands = {"<150": (20, 150), "150-600": (150, 600), "600-2.5k": (600, 2500), "2.5k-8k": (2500, 8000), ">8k": (8000, 20000)}
    tot = spec[(f >= 20) & (f < 20000)].sum()
    out = {k: round(10 * math.log10(spec[(f >= a) & (f < b)].sum() / tot + 1e-12), 1) for k, (a, b) in bands.items()}
    out["centroid_hz"] = round(cent)
    return out

if __name__ == "__main__":
    # 自我測試：量三支 pressure 參考檔的頻譜，順便驗證 finalize 能把 LRA 壓進 3 LU
    for f in ["pressureSamples_child.aif", "pressureSamples_wind.aif", "pressureSamples_water.aif"]:
        x = load(f)
        print(f, "LUFS", round(lufs(x), 1), spectral_summary(x))
    a = load(os.path.join(TRAVEL, "01_飛機與機場/FF_MT_airplane_foley_runway_riser.wav"))
    b = load(os.path.join(TRAVEL, "05_自行車與步行/ASO_foley_walking_outside.wav"))
    y = xfade_concat([norm_lufs(b, -20), norm_lufs(a, -20)], 4.0)
    y = reverb(y, 2.0, 4000, 20, 0.25)
    y = finalize(y)
    p = write(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_selftest.wav"), y, mp3=False)
    r = measure(p); print("selftest", r, "ok" if check(r) else "FAIL")
