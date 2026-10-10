#!/usr/bin/env python
"""
語句此起彼落 → 小星星氛圍尾聲（縮短版，參考 20260811_子翎測試剪輯輸出.mp3 的骨架）
段落：
  A  0–30 s   稀疏，一次一人，問答式
  B  30–70 s  變密，兩三人重疊，ㄅㄆㄇㄈ 音節當標點，tape echo、reverse delay、整句反轉、slip
  C  70–95 s  語句變稀，「ㄅㄆㄇㄈ」四聲部 phase 低聲爬進來，小星星氛圍 78 s 起淡入
  D  95–135 s 只剩小星星氛圍（低八度慢速＋原速漂移，低通、大殘響、wow），118 s 輕微重同步，尾端淡出
"""
import os, math, json
import numpy as np, soundfile as sf, librosa
from scipy.signal import fftconvolve, butter, lfilter

SRC = os.path.expanduser("~/Library/Mobile Documents/com~apple~CloudDocs/Documents/03_Projects_Operations/Active/ITRI_工研院藝術進駐/錄音")
OUT = os.path.join(SRC, "效果測試_20260902")
SR = 48000
DUR = 135.0
N = int(DUR * SR)
rng = np.random.default_rng(2026)

# ------------------------------------------------------------ 工具
def load(name, sr=SR):
    y, s = sf.read(os.path.join(SRC, name), always_2d=True)
    y = y.mean(axis=1)
    if s != sr:
        y = librosa.resample(y, orig_sr=s, target_sr=sr)
    return y

def phrases(y, sr=SR, top_db=30, gap=0.35, min_len=0.3, pad=0.06):
    iv = librosa.effects.split(y, top_db=top_db, frame_length=2048, hop_length=512)
    out = []
    for s, e in iv:
        s, e = s / sr, e / sr
        if out and s - out[-1][1] < gap:
            out[-1][1] = e
        else:
            out.append([s, e])
    res = []
    for s, e in out:
        if e - s < min_len:
            continue
        a = max(0, s - pad); b = min(len(y) / sr, e + pad)
        seg = y[int(a * sr):int(b * sr)].copy()
        f = int(0.01 * sr)
        seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
        seg /= (np.sqrt(np.mean(seg ** 2)) + 1e-9) / 0.06   # 統一到約 −24 dBFS RMS
        res.append(seg)
    return res

def cubic_read_noloop(src, pos):
    L = len(src)
    valid = (pos >= 1) & (pos < L - 2)
    p = np.clip(pos, 1, L - 3)
    i1 = np.floor(p).astype(np.int64); f = p - i1
    p0, p1, p2, p3 = src[i1 - 1], src[i1], src[i1 + 1], src[i1 + 2]
    out = p1 + 0.5 * f * (p2 - p0 + f * (2 * p0 - 5 * p1 + 4 * p2 - p3 + f * (3 * (p1 - p2) + p3 - p0)))
    return out * valid

def vari(seg, cents):
    """非循環 varispeed；cents 可以是常數或與輸出等長的陣列（輸出長度依平均速率估）。"""
    if np.isscalar(cents):
        rate = 2 ** (cents / 1200)
        n_out = int(len(seg) / rate)
        pos = np.arange(n_out) * rate
    else:
        rate = 2 ** (np.asarray(cents) / 1200)
        pos = np.cumsum(rate)
        n_out = int(np.searchsorted(pos, len(seg)))
        pos = pos[:n_out]
    return cubic_read_noloop(seg, pos)

def wow_curve(n, depth_cents, rate_hz, sr=SR, seed=None):
    r = np.random.default_rng(seed)
    n_ctrl = int(n / sr * 50) + 2
    x = np.zeros(n_ctrl); v = 0.0
    for k in range(1, n_ctrl):
        v += -rate_hz * 2 * v / 50 + depth_cents * math.sqrt(rate_hz / 50) * 2 * r.standard_normal()
        v = max(-2 * depth_cents, min(2 * depth_cents, v))
        x[k] = v
    return np.interp(np.arange(n) / sr, np.arange(n_ctrl) / 50, x)

def onepole_lp(x, hz, sr=SR):
    b, a = butter(1, hz / (sr / 2))
    return lfilter(b, a, x)

def echo(seg, delay_s, fb=0.45, lp_hz=2800, taps=10, sr=SR):
    """磁帶式回聲：每次回饋都再過一次低通，非遞迴展開。"""
    d = int(delay_s * sr)
    out = np.zeros(len(seg) + taps * d)
    out[:len(seg)] += seg
    cur = seg.copy()
    for k in range(1, taps + 1):
        cur = onepole_lp(cur, lp_hz) * fb
        out[k * d:k * d + len(cur)] += cur
    return out

def reverse_delay(seg, delay_s, fb=0.55, lp_hz=3000, taps=8):
    """反轉 → 回聲 → 再反轉：回聲出現在本音之前（swell in）。回傳 (音訊, 本音在陣列中的起點)。"""
    e = echo(seg[::-1], delay_s, fb, lp_hz, taps)[::-1]
    return e, len(e) - len(seg)

def make_ir(rt60, sr=SR, lp_hz=6000, seed=0):
    r = np.random.default_rng(seed)
    n = int(rt60 * 1.3 * sr)
    t = np.arange(n) / sr
    env = 10 ** (-3 * t / rt60)
    ir = np.stack([r.standard_normal(n), r.standard_normal(n)], axis=1) * env[:, None]
    ir[:, 0] = onepole_lp(ir[:, 0], lp_hz); ir[:, 1] = onepole_lp(ir[:, 1], lp_hz)
    ir[:int(0.005 * sr)] *= 0.2
    ir /= np.sqrt((ir ** 2).sum(axis=0)).max()
    return ir

def reverb(st, ir):
    L = fftconvolve(st[:, 0], ir[:, 0]); R = fftconvolve(st[:, 1], ir[:, 1])
    return np.stack([L, R], axis=1)

def saturate(x, drive=1.6):
    return np.tanh(drive * x) / math.tanh(drive)

def place(bus, mono, t, pan, gain=1.0):
    n0 = int(t * SR)
    if n0 >= len(bus) or n0 + len(mono) <= 0:
        return
    if n0 < 0:
        mono = mono[-n0:]; n0 = 0
    seg = mono[:len(bus) - n0]
    th = (pan + 1) / 2 * math.pi / 2
    bus[n0:n0 + len(seg), 0] += seg * math.cos(th) * gain
    bus[n0:n0 + len(seg), 1] += seg * math.sin(th) * gain

# ------------------------------------------------------------ 素材
speakers = {
    "阿瑤朗讀": dict(file="阿瑤朗讀.wav", pan=-0.55, cents=-4),
    "柏成朗讀": dict(file="柏成朗讀.wav", pan=0.55, cents=+3),
    "小軒朗讀": dict(file="小軒朗讀.wav", pan=-0.15, cents=+7),
    "柏豪ㄅㄆㄇ": dict(file="柏豪ㄅㄆㄇ.wav", pan=0.25, cents=-9),
    "阿瑤ㄅㄆㄇ": dict(file="阿瑤ㄅㄆㄇ.wav", pan=-0.35, cents=+5),
    "小軒ㄅㄆㄇ": dict(file="小軒ㄅㄆㄇ.wav", pan=0.05, cents=-2),
}
pool = {}
for k, v in speakers.items():
    y = load(v["file"])
    top = 30 if "朗讀" in k else 32
    gap = 0.35 if k != "小軒ㄅㄆㄇ" else 0.12   # 小軒念得很連，用小間隔切
    ph = phrases(y, top_db=top, gap=gap)
    pool[k] = ph
    print(k, len(ph), "phrases", [round(len(p) / SR, 1) for p in ph][:12])

bh = load("柏豪ㄅㄆㄇ.wav")
BPMF = bh[int(0.10 * SR):int(2.45 * SR)].copy()
f = int(0.012 * SR); BPMF[:f] *= np.linspace(0, 1, f); BPMF[-f:] *= np.linspace(1, 0, f)
xx = load("中藥行小星星.wav")
XA = xx[int(0.52 * SR):int(19.90 * SR)].copy(); XA[:f] *= np.linspace(0, 1, f); XA[-f:] *= np.linspace(1, 0, f)

# ------------------------------------------------------------ 匯流排
dry = np.zeros((N, 2)); echo_bus = np.zeros((N, 2)); hall_send = np.zeros((N, 2)); bed = np.zeros((N, 2))
cues = []

def density(t):
    """相鄰語句起點的平均間隔（秒）。"""
    if t < 30:  return 2.6
    if t < 45:  return 1.4
    if t < 62:  return 0.8
    if t < 72:  return 1.1
    if t < 85:  return 1.9
    if t < 95:  return 3.2
    return None

def pick_speaker(t, last):
    names = list(speakers)
    if t < 30:
        cand = ["阿瑤朗讀", "柏成朗讀", "小軒朗讀", "柏豪ㄅㄆㄇ"]
    else:
        cand = names
    cand = [c for c in cand if c != last] or cand
    w = np.array([1.0 if "朗讀" in c else (1.4 if t >= 30 else 0.6) for c in cand])
    return rng.choice(cand, p=w / w.sum())

t = 0.8; last = None; idx = {k: 0 for k in speakers}
order = {k: rng.permutation(len(v)) for k, v in pool.items()}
while True:
    gap = density(t)
    if gap is None:
        break
    spk = pick_speaker(t, last)
    ph = pool[spk][order[spk][idx[spk] % len(pool[spk])]]; idx[spk] += 1
    cfg = speakers[spk]
    # 每句：說話者固定微 detune ＋ 慢速 wow
    cents = cfg["cents"] + wow_curve(int(len(ph) * 1.05), 5, 0.3, seed=int(rng.integers(1 << 30)))[:len(ph)]
    seg = vari(ph, cents)
    pan = float(np.clip(cfg["pan"] + rng.normal(0, 0.25), -0.9, 0.9))
    fx = "dry"
    r = rng.random()
    if 30 <= t < 95 and r < 0.18:
        fx = "reverse"; seg = seg[::-1]
    if t >= 30 and 0.18 <= r < 0.40:
        fx = "echo"
    if r >= 0.40 and r < 0.55 and t >= 12:
        fx = "revdelay"
    if 48 <= t < 62 and rng.random() < 0.22:
        fx += "+slip"   # 句中突然減速滑落
        n = len(seg); k0 = int(n * rng.uniform(0.3, 0.6))
        slip = np.zeros(n); u = np.linspace(0, 1, n - k0)
        slip[k0:] = -700 * u ** 1.5
        seg = vari(seg, slip)
    gain = 10 ** (rng.uniform(-4, 1) / 20)
    gain *= 10 ** ({True: 0}.get(t < 30, 0) / 20)
    if 30 <= t < 45: gain *= 10 ** (-2 / 20)
    if 45 <= t < 72: gain *= 10 ** (-6 / 20)     # 密集段整體壓 6 dB
    if 72 <= t < 85: gain *= 10 ** (-3 / 20)
    if t >= 85:
        gain *= 10 ** (-(t - 85) / 10 * 12 / 20)   # 85 s 起每 10 秒退 12 dB
    if fx.startswith("revdelay"):
        e, start = reverse_delay(seg, rng.choice([0.31, 0.42, 0.57]))
        place(dry, e, t - start / SR, pan, gain * 0.9)
        place(hall_send, e, t - start / SR, pan, gain * 0.35)
    elif fx.startswith("echo"):
        place(dry, seg, t, pan, gain)
        e = echo(seg, rng.choice([0.29, 0.38, 0.51]), fb=rng.uniform(0.35, 0.55), lp_hz=rng.uniform(1800, 3200))
        place(echo_bus, e, t, -pan * 0.6, gain * 0.7)
        place(hall_send, e, t, pan, gain * 0.25)
    else:
        place(dry, seg, t, pan, gain)
        place(hall_send, seg, t, pan, gain * (0.18 if t < 70 else 0.35))
    cues.append((round(t, 2), spk, fx, round(len(seg) / SR, 2), round(pan, 2)))
    last = spk
    inc = gap * rng.uniform(0.45, 1.6)          # 有上下限，不會出現長空白
    if os.environ.get('DEBUG'): print(f'  t={t:6.2f} {spk} {fx} len={len(seg)/SR:.2f} inc={inc:.2f}')
    t += inc

# 最後一句：長反轉尾巴收進小星星
spk = "阿瑤朗讀"; ph = pool[spk][order[spk][3]]
e, start = reverse_delay(vari(ph, -4), 0.62, fb=0.7, taps=12)
place(dry, e, 97.5 - start / SR, -0.3, 0.8); place(hall_send, e, 97.5 - start / SR, -0.3, 0.8)
cues.append((97.5, spk, "revdelay-long(final)", round(len(e) / SR, 2), -0.3))

# C 段：「ㄅㄆㄇㄈ」四聲部 phase，72–100 s，低聲
offs = [0, 6, -6, 12]
for i, c in enumerate(offs):
    n_loop = int(28 * SR)
    reps = int(np.ceil(n_loop / len(BPMF))) + 1
    lp = np.tile(BPMF, reps)
    seg = vari(lp, c + wow_curve(len(lp), 3, 0.2, seed=100 + i))[:n_loop]
    env = np.ones(len(seg)); a = int(8 * SR); d = int(10 * SR)
    env[:a] = np.linspace(0, 1, a); env[-d:] = np.linspace(1, 0, d)
    seg = seg * env * 0.35
    place(dry, seg, 72, [-0.7, -0.25, 0.25, 0.7][i], 1.0)
    place(hall_send, seg, 72, [-0.7, -0.25, 0.25, 0.7][i], 0.5)

# 小星星氛圍：78 s 淡入到結尾
bed_start = 78.0
bed_len = DUR - bed_start
n_bed = int(bed_len * SR)
def bed_voice(rate_base, cents_depth, seed, pan, gain, resync_at=118.0, tau=3.0):
    reps = int(np.ceil(n_bed * rate_base * 1.2 / len(XA))) + 2
    src = np.tile(XA, reps)
    w = wow_curve(n_bed, cents_depth, 0.05, seed=seed)
    tt = np.arange(n_bed) / SR + bed_start
    m = tt >= resync_at
    w[m] = w[m][0] * np.exp(-(tt[m] - resync_at) / tau)     # 118 s 起慢慢回到共同速度
    rate = rate_base * 2 ** (w / 1200)
    pos = np.cumsum(rate)
    seg = cubic_read_noloop(src, pos)
    seg = onepole_lp(onepole_lp(seg, 2600), 2600)
    env = np.ones(n_bed); a = int(18 * SR); d = int(8 * SR)
    env[:a] = np.linspace(0, 1, a) ** 2; env[-d:] = np.linspace(1, 0, d)
    place(bed, seg * env * gain, bed_start, pan)
bed_voice(0.5, 8, 11, 0.0, 0.9)      # 低八度慢速
bed_voice(1.0, 10, 12, -0.5, 0.45)   # 原速漂移左
bed_voice(1.0, 10, 13, 0.5, 0.45)    # 原速漂移右

# ------------------------------------------------------------ 混音
if os.environ.get('DEBUG'):
    np.savez(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'buses.npz'), dry=dry, echo=echo_bus, hall=hall_send, bed=bed)
room = make_ir(0.7, lp_hz=5000, seed=1)
hall = make_ir(3.8, lp_hz=3500, seed=2)
mix = np.zeros((N, 2))
sp = saturate(dry * 1.0, 1.6) + echo_bus * 0.9
mix += sp
mix += reverb(sp, room)[:N] * 0.22
mix += reverb(hall_send, hall)[:N] * 0.55
bed_wet = reverb(bed, hall)[:N]
mix += saturate(bed * 0.7 + bed_wet * 0.6, 1.3) * 0.9
# 極低的磁帶底噪，跟著 bed 進來
hiss = np.stack([rng.standard_normal(N), rng.standard_normal(N)], axis=1)
hiss = np.stack([onepole_lp(hiss[:, 0], 4000), onepole_lp(hiss[:, 1], 4000)], axis=1)
henv = np.clip((np.arange(N) / SR - 70) / 20, 0, 1)
mix += hiss * henv[:, None] * 10 ** (-58 / 20)
# 收尾與整體
fo = int(6 * SR); mix[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.5
mix[:int(0.01 * SR)] *= np.linspace(0, 1, int(0.01 * SR))[:, None]
mix = np.tanh(mix * 1.2) / math.tanh(1.2)
mix /= np.abs(mix).max() / 10 ** (-1 / 20)

name = "11_語句此起彼落_小星星尾聲_v1.wav"
sf.write(os.path.join(OUT, name), mix, SR, subtype="PCM_24")
json.dump(cues, open(os.path.join(OUT, "11_cue_sheet.json"), "w"), ensure_ascii=False, indent=0)
print("wrote", name, f"{N/SR:.1f}s  peak {20*math.log10(np.abs(mix).max()):.1f} dBFS  cues {len(cues)}")

# 時間軸圖
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib import font_manager
fp = None
for cand in ["/System/Library/Fonts/PingFang.ttc", "/System/Library/Fonts/STHeiti Light.ttc", "/Library/Fonts/Arial Unicode.ttf"]:
    if os.path.exists(cand): fp = font_manager.FontProperties(fname=cand); break
fig, ax = plt.subplots(2, 1, figsize=(16, 7), sharex=True, gridspec_kw=dict(height_ratios=[3, 1]))
names = list(speakers)
colors = dict(dry="#555", reverse="#d62728", echo="#1f77b4", revdelay="#2ca02c")
for tt, spk, fx, ln, pan in cues:
    y0 = names.index(spk) if spk in names else 0
    c = colors.get(fx.split("+")[0].split("-")[0], "#999")
    ax[0].barh(y0, ln, left=tt, height=0.6, color=c, alpha=0.8)
    if "slip" in fx: ax[0].text(tt, y0 + 0.35, "slip", fontsize=7)
ax[0].set_yticks(range(len(names))); ax[0].set_yticklabels(names, fontproperties=fp)
ax[0].axvspan(72, 100, color="orange", alpha=0.08); ax[0].text(73, len(names) - 0.6, "ㄅㄆㄇㄈ phase", fontproperties=fp, fontsize=9)
ax[0].axvspan(78, DUR, color="purple", alpha=0.08); ax[0].text(100, len(names) - 0.6, "小星星氛圍", fontproperties=fp, fontsize=9)
ax[0].set_title("11 時間軸：灰=dry 藍=echo 綠=reverse delay 紅=整句反轉", fontproperties=fp)
rms = librosa.feature.rms(y=mix.mean(axis=1), frame_length=4800, hop_length=2400)[0]
ax[1].plot(np.arange(len(rms)) * 2400 / SR, 20 * np.log10(rms + 1e-9)); ax[1].set_ylabel("dBFS"); ax[1].set_xlabel("s"); ax[1].grid(alpha=.3)
fig.tight_layout(); fig.savefig(os.path.join(OUT, "11_時間軸.png"), dpi=80)
