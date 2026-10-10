#!/usr/bin/env python
"""
《節奏繞纏》背景 pad 生成（2026-09-08）

來源只有兩個既有素材：
  中藥行小星星.wav                 人聲吟唱，取「主音」與「五度音」的音框，paulstretch 拉長成無旋律的 pad
  Dicy2_memory/呼吸盤帶拼貼_stereo.wav  呼吸層，整場常駐

每幕一支可 loop 的 wav。檔案開頭 HEAD_S 秒烘進上一幕的尾巴（等功率交叉淡化），
Live 裡 clip Start 設 0、Loop Start 設 HEAD_S，就能無縫換幕。
所有參數集中在下面的 CONFIG，改完重跑即可。
"""
import sys, json, pathlib, math
import numpy as np, soundfile as sf, librosa
from scipy.signal import butter, sosfilt, resample_poly

SRC = pathlib.Path("/Users/zonesound/Library/Mobile Documents/com~apple~CloudDocs/Documents/03_Projects_Operations/Active/ITRI_工研院藝術進駐/錄音")
STAR = SRC / "中藥行小星星.wav"
BREATH = SRC / "Dicy2_memory/呼吸盤帶拼貼_stereo.wav"
OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "out_pads")
OUT.mkdir(parents=True, exist_ok=True)
SR = 44100
rng = np.random.default_rng(20260908)

CONFIG = dict(
    STRETCH=60.0,          # paulstretch 倍率
    WIN=32768,             # paulstretch 視窗（0.74 s），越大越平滑
    HEAD_S=8.0,            # 每檔開頭烘進上一幕尾巴的秒數
    LOOP_XF_S=6.0,         # body 首尾 loop 交叉淡化
    BREATH_DB=-20.0,       # 呼吸層相對 pad 峰值的音量
    # ---- 磁帶路線（2026-09-08 第二版）----
    WOW_CENTS=12.0,        # 慢速音高晃動幅度（磁帶 wow），第一版是 4
    WOW_PERIOD_S=23.0,
    FLUTTER_HZ=7.0, FLUTTER_CENTS=2.0,   # 細抖
    DETUNE_CENTS=6.0,      # 兩份副本各 ±6 cents，互相打拍
    HISS_DB=-46.0,         # 磁帶嘶聲相對 pad 峰值
    SAT_DRIVE=1.8,         # 飽和量（第一版 1.3）
    ACT1_LP=3000.0, ACT2_LP=4500.0, ACT3_OPEN_LP=1500.0,
    # ---- 第三幕顆粒版（03C）----
    GRAIN_MS=(150, 300), GRAIN_DENSITY=14.0, GRAIN_PITCH_JITTER=5.0, GRAIN_LEN_S=330.0,
    SWELL_DB=2.0,          # 第一幕極慢漲落 ±dB
    SWELL_PERIOD_S=26.0,
    ACT1_LEN=360, ACT2_LEN=240, ACT0_LEN=240, END_LEN=20,
    # 第三幕 drone 低通「打開」的時間（秒，相對 drone 開始）。目標：柏豪出聲、星空淡入時打開。
    # 3A：scene 3 在黑場（8/24 約 06:54）就切，柏豪出聲約 10:22 到 10:40 ＝ +210 到 +225 秒
    ACT3A_OPEN_START=210.0, ACT3A_OPEN_END=270.0,
    # 3B：先只有呼吸，drone 在 ACT3B_DRONE_ENTER 秒後淡入（約 08:09），柏豪出聲 ＝ drone 後 +135 秒
    ACT3B_OPEN_START=135.0, ACT3B_OPEN_END=195.0,
    ACT3_LOOP_LEN=240,                            # 打開之後的 loop 區長度（Loop Start = 打開完成那一刻）
    ACT3B_DRONE_ENTER=75.0, ACT3B_DRONE_FADE=20.0, # 3B 版：黑場＋無聲影片先只有呼吸，drone 幾秒後進
    PEAK_DBFS=-1.0,
)

# ---------- helpers ----------
def db(x): return 10 ** (x / 20)

def sos_lp(fc, order=4): return butter(order, fc / (SR / 2), btype="low", output="sos")
def sos_hp(fc, order=4): return butter(order, fc / (SR / 2), btype="high", output="sos")
def filt(sos, x): return sosfilt(sos, x, axis=0) if x.ndim == 2 else sosfilt(sos, x)

def to_stereo(x):
    return np.stack([x, x], axis=1) if x.ndim == 1 else x

def fade(x, fin=0.0, fout=0.0):
    x = x.copy(); n = len(x)
    if fin > 0:
        k = min(n, int(fin * SR)); r = np.sin(np.linspace(0, np.pi / 2, k)) ** 2
        x[:k] *= r[:, None] if x.ndim == 2 else r
    if fout > 0:
        k = min(n, int(fout * SR)); r = np.cos(np.linspace(0, np.pi / 2, k)) ** 2
        x[-k:] *= r[:, None] if x.ndim == 2 else r
    return x

def loop_to(x, length_s, xf_s):
    """把 x 做成長度 length_s 的無縫 loop：先讓 x 自己首尾交叉淡化，再重複。"""
    n = int(length_s * SR); k = int(xf_s * SR)
    assert len(x) > 2 * k, "material too short for loop crossfade"
    body = x[:-k].copy()
    a = np.cos(np.linspace(0, np.pi / 2, k)) ** 2; b = 1 - a
    tail = x[-k:]
    body[:k] = body[:k] * b[:, None] + tail * a[:, None]   # 尾巴疊進開頭 → body 首尾連續
    reps = math.ceil(n / len(body)) + 1
    return np.tile(body, (reps, 1))[:n]

def peak_norm(x, dbfs):
    p = np.max(np.abs(x)); return x * (db(dbfs) / p) if p > 0 else x

def paulstretch(x, stretch, win):
    """Paul Nasca 的 paulstretch（相位隨機化）。x: (n, ch)。"""
    x = to_stereo(x); n, ch = x.shape
    half = win // 2
    w = 1 - np.linspace(-1, 1, win) ** 2; w = w ** 1.25          # paulstretch 原版視窗
    displace = half / stretch
    out_len = int(n * stretch) + win
    out = np.zeros((out_len, ch)); norm = np.zeros(out_len)
    pos = 0.0; o = 0
    # 不補零：視窗只讀真實輸入，否則輸出尾端會有 win*stretch 秒的漸弱（60 倍時約 45 秒），loop 會出現凹陷
    while o + win < out_len and pos + win <= n:
        i = int(pos)
        seg = x[i:i + win] * w[:, None]
        spec = np.fft.rfft(seg, axis=0)
        mag = np.abs(spec)
        ph = np.exp(1j * rng.uniform(0, 2 * np.pi, size=mag.shape))
        y = np.fft.irfft(mag * ph, n=win, axis=0) * w[:, None]
        out[o:o + win] += y; norm[o:o + win] += w ** 2
        o += half; pos += displace
    norm[norm < 1e-6] = 1
    return out[:o] / norm[:o, None]

def pitch_shift_oct(x, octaves):
    """整八度移調用重取樣（速度變、音高變；pad 用不在意長度）。"""
    if octaves == 0: return x
    if octaves < 0: return resample_poly(x, 2 ** (-octaves), 1, axis=0)   # 變慢 → 變低
    return resample_poly(x, 1, 2 ** octaves, axis=0)                      # 變快 → 變高

def tape_pitch(x, wow_cents, period_s, flutter_hz=0.0, flutter_cents=0.0, detune_cents=0.0, phase=None):
    """磁帶音高：慢 wow（正弦加一點隨機遊走）＋ 細抖 flutter ＋ 固定 detune。以變速重取樣近似。"""
    n = len(x); t = np.arange(n) / SR
    ph = rng.uniform(0, 2 * np.pi, 3) if phase is None else phase
    walk = np.cumsum(rng.normal(0, 1, n // 4410 + 2)); walk = np.interp(t, np.arange(len(walk)) * 0.1, walk)
    walk = walk / (np.std(walk) + 1e-9) * 0.35            # 隨機遊走佔 wow 的三分之一，讓晃動不那麼規律
    cents = wow_cents * (np.sin(2 * np.pi * t / period_s + ph[0]) * 0.75 + walk) \
          + flutter_cents * np.sin(2 * np.pi * flutter_hz * t + ph[1]) + detune_cents
    ratio = 2 ** (cents / 1200)
    src_pos = np.cumsum(ratio); src_pos -= src_pos[0]
    src_pos = src_pos[src_pos < n - 1]
    idx = np.arange(n)
    return np.stack([np.interp(src_pos, idx, x[:, c]) for c in range(x.shape[1])], axis=1)

def hiss(length_s, level_db):
    """磁帶嘶聲：粉紅偏的雜訊，1 到 6 kHz，左右不相關。"""
    n = int(length_s * SR)
    w = rng.normal(0, 1, (n, 2))
    w = filt(sos_hp(800, 2), filt(sos_lp(6000, 2), w))
    return peak_norm(w, level_db)

def swell(x, depth_db, period_s, phase=0.0):
    t = np.arange(len(x)) / SR
    g = db(depth_db * np.sin(2 * np.pi * t / period_s + phase))
    return x * g[:, None]

def soft_sat(x, drive=1.3):
    return np.tanh(x * drive) / np.tanh(drive)

# ---------- 1. 找主音與五度音的音框 ----------
star, sr0 = sf.read(STAR, always_2d=True)
assert sr0 == SR
mono = star.mean(axis=1)
f0, vflag, vprob = librosa.pyin(mono[: int(40 * SR)], fmin=80, fmax=900, sr=SR, frame_length=4096, hop_length=512)
hop_s = 512 / SR
times = np.arange(len(f0)) * hop_s

def midi_of(seg):
    v = seg[~np.isnan(seg)]; return float(np.median(librosa.hz_to_midi(v))) if len(v) else np.nan
# 主音證據：第一句最後一個音（19.90 s 前 1.2 s）與第一個音（0.52 到 1.3 s）
tonic_end = midi_of(f0[(times > 18.7) & (times < 19.9)])
tonic_start = midi_of(f0[(times > 0.55) & (times < 1.3)])
tonic_pc = round(tonic_end) % 12
report = dict(tonic_last_note_midi=tonic_end, tonic_first_note_midi=tonic_start,
              tonic_pitch_class=librosa.midi_to_note(60 + tonic_pc, octave=False))
print("tonic evidence:", report)

def frames_for_pc(pc, tol_cents=70):
    m = librosa.hz_to_midi(np.nan_to_num(f0, nan=0.0))
    ok = (~np.isnan(f0)) & (vprob > 0.6)
    dist = np.abs(((m - pc + 6) % 12) - 6) * 100
    return ok & (dist < tol_cents)

def extract(mask, min_run_s=0.15, xf_s=0.02, limit_s=None):
    """把符合 mask 的連續段切出來、短交叉淡化接成一段素材。"""
    runs = []; i = 0
    while i < len(mask):
        if mask[i]:
            j = i
            while j < len(mask) and mask[j]: j += 1
            if (j - i) * hop_s >= min_run_s: runs.append((times[i], times[j]))
            i = j
        else: i += 1
    # 片段之間用重疊交叉淡化接合（不是各自淡入淡出再接）：接點若有 40 ms 的靜音，拉長 60 倍會變成 2.4 秒的谷
    k = int(xf_s * SR); a = np.cos(np.linspace(0, np.pi / 2, k)) ** 2; b = 1 - a
    mat = np.zeros((0, 2))
    for s, e in runs:
        seg = star[int(s * SR): int(e * SR)]
        if len(mat) == 0: mat = seg.copy(); continue
        mat[-k:] = mat[-k:] * a[:, None] + seg[:k] * b[:, None]
        mat = np.concatenate([mat, seg[k:]])
    if limit_s: mat = mat[: int(limit_s * SR)]
    return mat, runs

tonic_mat, tonic_runs = extract(frames_for_pc(tonic_pc), xf_s=0.05, limit_s=7.0)
fifth_mat, fifth_runs = extract(frames_for_pc((tonic_pc + 7) % 12), xf_s=0.05, limit_s=6.0)
print(f"tonic material {len(tonic_mat)/SR:.2f}s from {len(tonic_runs)} runs; fifth {len(fifth_mat)/SR:.2f}s from {len(fifth_runs)} runs")
assert len(tonic_mat) / SR > 2.5 and len(fifth_mat) / SR > 2.0, "not enough tonic/fifth material"

# ---------- 2. 拉長 ----------
C = CONFIG
tonic_pad = paulstretch(tonic_mat, C["STRETCH"], C["WIN"])   # 原音域（約 7 min）
fifth_pad = paulstretch(fifth_mat, C["STRETCH"], C["WIN"])
print(f"stretched tonic {len(tonic_pad)/SR:.0f}s, fifth {len(fifth_pad)/SR:.0f}s")

from scipy.ndimage import uniform_filter1d
def level(x, win_s=2.0, smooth_s=3.0, max_gain_db=12.0):
    """慢速電平器：把 2 秒尺度的音量起伏壓平（歌者的強弱被拉長 60 倍後會變成十幾 dB 的谷）。
    pad 要的是平，動態交給 swell 與 Live。"""
    p = uniform_filter1d(np.mean(x ** 2, axis=1), int(win_s * SR), mode="nearest")
    env = np.sqrt(p) + 1e-9
    g = np.median(env) / env
    g = np.clip(g, db(-max_gain_db), db(max_gain_db))
    g = uniform_filter1d(g, int(smooth_s * SR), mode="nearest")
    return x * g[:, None]

def finish(x, lp=None, hp=None, sat=True):
    """磁帶路線：兩份副本各 ±DETUNE，各自獨立 wow/flutter → 打拍與晃動；再飽和。"""
    if hp: x = filt(sos_hp(hp), x)
    if lp: x = filt(sos_lp(lp), x)
    x = level(x)
    a = tape_pitch(x, C["WOW_CENTS"], C["WOW_PERIOD_S"], C["FLUTTER_HZ"], C["FLUTTER_CENTS"], +C["DETUNE_CENTS"])
    b = tape_pitch(x, C["WOW_CENTS"], C["WOW_PERIOD_S"] * 1.17, C["FLUTTER_HZ"] * 0.93, C["FLUTTER_CENTS"], -C["DETUNE_CENTS"])
    m = min(len(a), len(b)); x = (a[:m] + b[:m]) * 0.5
    if sat: x = soft_sat(peak_norm(x, -6), C["SAT_DRIVE"])
    return x

def granular(material, length_s, grain_ms, density, pitch_jitter_cents, rate=1.0, seed=1):
    """簡單的顆粒雲：從 material 隨機取位置、Hann 窗、每粒微 detune，rate 控整體八度（0.5 = 低八度）。
    density = 每秒幾粒；粒子大（150 到 300 ms）＋密度高 ＝ 平滑的雲，不會有顆粒節奏。"""
    r = np.random.default_rng(seed)
    n = int(length_s * SR); out = np.zeros((n + SR, 2))
    total = int(length_s * density)
    starts = np.sort(r.uniform(0, length_s, total)); idx = np.arange(len(material))
    for s in starts:
        g_len_out = int(r.uniform(*grain_ms) / 1000 * SR)
        ratio = rate * 2 ** (r.normal(0, pitch_jitter_cents) / 1200)
        g_len_in = int(g_len_out * ratio)
        if g_len_in >= len(material) - 1: continue
        p = int(r.uniform(0, len(material) - g_len_in - 1))
        src = np.linspace(p, p + g_len_in, g_len_out, endpoint=False)
        g = np.stack([np.interp(src, idx, material[:, c]) for c in range(2)], axis=1)
        g *= np.hanning(g_len_out)[:, None]
        pan = r.uniform(0.3, 0.7); g *= np.array([np.sqrt(1 - pan), np.sqrt(pan)])
        o = int(s * SR); out[o:o + g_len_out] += g
    return out[:n]

# ---------- 3. 呼吸層 ----------
breath, srb = sf.read(BREATH, always_2d=True); assert srb == SR
breath = filt(sos_hp(60), breath)
# 原檔最後約 5 秒是靜音（量測 −68 dBFS），loop 前切掉，只留到最後一個有聲樣本前 0.2 秒
nz = np.where(np.max(np.abs(breath), axis=1) > 1e-3)[0][-1]
breath = breath[: nz - int(0.2 * SR)]

def breath_layer(length_s, rel_db=C["BREATH_DB"]):
    b = loop_to(breath, length_s, 8.0)
    return peak_norm(b, C["PEAK_DBFS"] + rel_db)

# ---------- 4. 各幕 body（穩態、可 loop） ----------
def mk_body(layers, length_s, breath_db=C["BREATH_DB"]):
    mix = None
    for x, gain_db in layers:
        y = loop_to(x, length_s, C["LOOP_XF_S"]) * db(gain_db)
        mix = y if mix is None else mix + y
    mix = peak_norm(mix, C["PEAK_DBFS"] - 0.5)
    mix = mix + breath_layer(length_s, breath_db) + hiss(length_s, C["PEAK_DBFS"] + C["HISS_DB"])
    return peak_norm(mix, C["PEAK_DBFS"])

# 第一幕：主音，原八度＋低八度，胸腔感
act1 = mk_body([(finish(tonic_pad, lp=C["ACT1_LP"]), 0.0),
                (finish(pitch_shift_oct(tonic_pad, -1), lp=1800), -2.0)], C["ACT1_LEN"])
swell_period = C["ACT1_LEN"] / round(C["ACT1_LEN"] / C["SWELL_PERIOD_S"])   # 週期整除 loop 長度，接縫不跳
act1 = peak_norm(swell(act1, C["SWELL_DB"], swell_period), C["PEAK_DBFS"])

# 第二幕：主音＋五度，高一個八度，更薄更亮
act2 = mk_body([(finish(pitch_shift_oct(tonic_pad, +1), lp=C["ACT2_LP"], hp=200), 0.0),
                (finish(pitch_shift_oct(fifth_pad, +1), lp=C["ACT2_LP"], hp=200), -4.0)], C["ACT2_LEN"])

# 第三幕：低八度＋再低八度的主音 drone；低通從 300 Hz 打開到 1.5 kHz 並 +3 dB
low1 = finish(pitch_shift_oct(tonic_pad, -1), sat=False)
low2 = finish(pitch_shift_oct(tonic_pad, -2), sat=False)
L = C["ACT3_LOOP_LEN"]
body_open = mk_body([(filt(sos_lp(C["ACT3_OPEN_LP"]), low1), 0.0), (filt(sos_lp(300), low2), -1.0),
                     (finish(tonic_pad, lp=C["ACT3_OPEN_LP"]), -9.0)], L, breath_db=C["BREATH_DB"] - 4)   # 無縫 loop，長 L
closed_long = mk_body([(filt(sos_lp(300), low1), 0.0), (filt(sos_lp(200), low2), -1.0)], 300, breath_db=C["BREATH_DB"] - 4)

# 03C 顆粒版：同一段主音素材，粒子 150 到 300 ms、每秒 14 粒、音高鎖 C ±5 cents；低八度為主
g_low1 = level(granular(tonic_mat, C["GRAIN_LEN_S"], C["GRAIN_MS"], C["GRAIN_DENSITY"], C["GRAIN_PITCH_JITTER"], rate=0.5, seed=11))
g_low2 = level(granular(tonic_mat, C["GRAIN_LEN_S"], C["GRAIN_MS"], C["GRAIN_DENSITY"] * 0.7, C["GRAIN_PITCH_JITTER"], rate=0.25, seed=12))
g_orig = level(granular(tonic_mat, C["GRAIN_LEN_S"], C["GRAIN_MS"], C["GRAIN_DENSITY"], C["GRAIN_PITCH_JITTER"], rate=1.0, seed=13))
g_low1, g_low2, g_orig = (soft_sat(peak_norm(v, -6), 1.3) for v in (g_low1, g_low2, g_orig))
gran_open = mk_body([(filt(sos_lp(2000), g_low1), 0.0), (filt(sos_lp(300), g_low2), -2.0),
                     (filt(sos_lp(2500), g_orig), -8.0)], L, breath_db=C["BREATH_DB"] - 4)
gran_closed = mk_body([(filt(sos_lp(400), g_low1), 0.0), (filt(sos_lp(200), g_low2), -1.0)], 300, breath_db=C["BREATH_DB"] - 4)

def make_act3(open_start, open_end, closed_long=closed_long, body_open=body_open):
    """關閉狀態 drone → 在 open_start 到 open_end 之間平滑打開 → 接無縫 loop 的打開狀態。
    回傳 (audio, loop_start_s)；loop 區 = [open_end, end)。"""
    T = int(open_end * SR)
    drone_closed = closed_long[:T]
    # 過渡段的 open 成分取自同一個 loop 並旋轉相位，讓過渡結束那一刻剛好接到 body_open[0]
    open_in_transition = body_open[(np.arange(T) - T) % len(body_open)]
    t = np.arange(T) / SR
    m = np.clip((t - open_start) / (open_end - open_start), 0, 1)
    m = 0.5 - 0.5 * np.cos(np.pi * m)                              # 平滑打開
    transition = drone_closed * (1 - m)[:, None] * db(-3) + open_in_transition * m[:, None]   # 打開後比關閉時大 3 dB
    x = np.concatenate([transition, body_open])
    return x * (db(C["PEAK_DBFS"]) / np.max(np.abs(x))), open_end

act3a, act3a_loop = make_act3(C["ACT3A_OPEN_START"], C["ACT3A_OPEN_END"])
act3b_core, act3b_loop = make_act3(C["ACT3B_OPEN_START"], C["ACT3B_OPEN_END"])
act3c, act3c_loop = make_act3(C["ACT3A_OPEN_START"], C["ACT3A_OPEN_END"], gran_closed, gran_open)

# 待機與結尾：只有呼吸
act0 = breath_layer(C["ACT0_LEN"], rel_db=0.0) * db(-6)      # 檔案本身不推滿，Live 再拉
ending = fade(breath_layer(C["END_LEN"], rel_db=0.0) * db(-6), 0, 12.0)

# ---------- 5. 組檔：開頭烘進上一幕尾巴 ----------
H = int(C["HEAD_S"] * SR)
def with_head(prev_body, cur_body, append_tail=True):
    """開頭 H 秒＝上一幕尾巴淡出＋本幕淡入。append_tail=True 時尾端補回 body[:H]，
    使 Loop 區 [H, end) 剛好是 body 的一個旋轉（無縫）。"""
    a = np.cos(np.linspace(0, np.pi / 2, H)) ** 2; b = 1 - a
    prev_tail = prev_body[-H:] if prev_body is not None else np.zeros((H, 2))
    head = prev_tail * a[:, None] + cur_body[:H] * b[:, None]
    parts = [head, cur_body[H:]] + ([cur_body[:H]] if append_tail else [])
    return np.concatenate(parts)

files, loop_start = {}, {}
files["00_待機_呼吸層_loop"] = act0;                              loop_start["00_待機_呼吸層_loop"] = 0.0
files["01_第一幕_主音pad_head8s"] = with_head(act0, act1);        loop_start["01_第一幕_主音pad_head8s"] = C["HEAD_S"]
files["02_第二幕_空五度pad_head8s"] = with_head(act1, act2);      loop_start["02_第二幕_空五度pad_head8s"] = C["HEAD_S"]
# head 是「原地」取代前 HEAD_S 秒，所以檔案時間軸 = act3 時間軸，loop 起點不必加 HEAD_S
files["03A_第三幕_drone_立即進入_head8s"] = with_head(act2, act3a, append_tail=False)
loop_start["03A_第三幕_drone_立即進入_head8s"] = act3a_loop
# 3B：黑場與無聲影片先只有呼吸，drone 在 ACT3B_DRONE_ENTER 秒後淡入
b_only = breath_layer(C["ACT3B_DRONE_ENTER"], rel_db=C["BREATH_DB"] - 4)
act3b = np.concatenate([b_only, fade(act3b_core, C["ACT3B_DRONE_FADE"], 0)])
files["03B_第三幕_黑場先呼吸_drone75s後進_head8s"] = with_head(act2, act3b, append_tail=False)
loop_start["03B_第三幕_黑場先呼吸_drone75s後進_head8s"] = C["ACT3B_DRONE_ENTER"] + act3b_loop
files["03C_第三幕_顆粒版_立即進入_head8s"] = with_head(act2, act3c, append_tail=False)
loop_start["03C_第三幕_顆粒版_立即進入_head8s"] = act3c_loop
files["05_結尾_呼吸收尾_20s"] = ending;                            loop_start["05_結尾_呼吸收尾_20s"] = None

# 主音／五度音素材另存（給 Granulator III、Iota 用）
MAT = OUT / "素材"; MAT.mkdir(exist_ok=True)
sf.write(MAT / f"小星星_主音{report['tonic_pitch_class']}_音框拼接_{len(tonic_mat)/SR:.1f}s.wav", peak_norm(tonic_mat, -1), SR, subtype="PCM_24")
sf.write(MAT / f"小星星_五度音_音框拼接_{len(fifth_mat)/SR:.1f}s.wav", peak_norm(fifth_mat, -1), SR, subtype="PCM_24")
sf.write(MAT / "小星星_主音_paulstretch60x_原八度_乾.wav", peak_norm(tonic_pad, -1), SR, subtype="PCM_24")

meta = {"config": C, "tonic": report,
        "tonic_runs_s": [[round(s, 2), round(e, 2)] for s, e in tonic_runs],
        "fifth_runs_s": [[round(s, 2), round(e, 2)] for s, e in fifth_runs], "files": {}}
for name, x in files.items():
    x = np.clip(x, -1, 1)
    p = OUT / f"{name}.wav"
    sf.write(p, x, SR, subtype="PCM_24")
    meta["files"][p.name] = {"seconds": round(len(x) / SR, 2), "peak_dbfs": round(20 * np.log10(np.max(np.abs(x)) + 1e-12), 2),
                             "live_loop_start_s": loop_start[name]}
    print("wrote", p.name, meta["files"][p.name])
(OUT / "render_meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1))
