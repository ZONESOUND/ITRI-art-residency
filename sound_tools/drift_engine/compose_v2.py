#!/usr/bin/env python
"""
v2：ㄅㄆㄇㄈ 三人交錯在最前面 → 37 個注音符號依序輪流、逐漸變成三人同念但相位拉開 →
單詞（朗讀）模糊墊底 → 小星星第一句以耦合漂移＋重同步當尾聲。總長 100 秒。
"""
import os, math, json
import numpy as np, soundfile as sf, librosa
from scipy.signal import fftconvolve, butter, lfilter

SP = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.expanduser("~/Library/Mobile Documents/com~apple~CloudDocs/Documents/03_Projects_Operations/Active/ITRI_工研院藝術進駐/錄音")
OUT = os.path.join(SRC, "效果測試_20260902")
SR = 48000
DUR = 100.0
N = int(DUR * SR)
rng = np.random.default_rng(7)
SYM = list("ㄅㄆㄇㄈㄉㄊㄋㄌㄍㄎㄏㄐㄑㄒㄓㄔㄕㄖㄗㄘㄙㄧㄨㄩㄚㄛㄜㄝㄞㄟㄠㄡㄢㄣㄤㄥㄦ")

# ------------------------------------------------------------ 工具（與 v1 相同）
def load(name, sr=SR):
    y, s = sf.read(os.path.join(SRC, name), always_2d=True); y = y.mean(axis=1)
    return librosa.resample(y, orig_sr=s, target_sr=sr) if s != sr else y

def fade(seg, ms=10):
    f = int(ms * SR / 1000); seg = seg.copy()
    seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
    return seg

def norm_rms(seg, target=0.06):
    return seg / (np.sqrt(np.mean(seg ** 2)) + 1e-9) * target

def cubic_noloop(src, pos):
    L = len(src); valid = (pos >= 1) & (pos < L - 2); p = np.clip(pos, 1, L - 3)
    i1 = np.floor(p).astype(np.int64); f = p - i1
    p0, p1, p2, p3 = src[i1 - 1], src[i1], src[i1 + 1], src[i1 + 2]
    return (p1 + 0.5 * f * (p2 - p0 + f * (2 * p0 - 5 * p1 + 4 * p2 - p3 + f * (3 * (p1 - p2) + p3 - p0)))) * valid

def cubic_loop(src, pos):
    L = len(src); pos = np.mod(pos, L); i1 = np.floor(pos).astype(np.int64); f = pos - i1
    p0, p1, p2, p3 = src[(i1 - 1) % L], src[i1], src[(i1 + 1) % L], src[(i1 + 2) % L]
    return p1 + 0.5 * f * (p2 - p0 + f * (2 * p0 - 5 * p1 + 4 * p2 - p3 + f * (3 * (p1 - p2) + p3 - p0)))

def vari(seg, cents):
    if np.isscalar(cents):
        rate = 2 ** (cents / 1200); pos = np.arange(int(len(seg) / rate)) * rate
    else:
        rate = 2 ** (np.asarray(cents) / 1200); pos = np.cumsum(rate); pos = pos[:int(np.searchsorted(pos, len(seg)))]
    return cubic_noloop(seg, pos)

def wow_curve(n, depth_cents, rate_hz, seed=None):
    r = np.random.default_rng(seed); n_ctrl = int(n / SR * 50) + 2; x = np.zeros(n_ctrl); v = 0.0
    for k in range(1, n_ctrl):
        v += -rate_hz * 2 * v / 50 + depth_cents * math.sqrt(rate_hz / 50) * 2 * r.standard_normal()
        v = max(-2 * depth_cents, min(2 * depth_cents, v)); x[k] = v
    return np.interp(np.arange(n) / SR, np.arange(n_ctrl) / 50, x)

def onepole_lp(x, hz):
    b, a = butter(1, hz / (SR / 2)); return lfilter(b, a, x)

def echo(seg, delay_s, fb=0.45, lp_hz=2800, taps=10):
    d = int(delay_s * SR); out = np.zeros(len(seg) + taps * d); out[:len(seg)] += seg; cur = seg.copy()
    for k in range(1, taps + 1):
        cur = onepole_lp(cur, lp_hz) * fb; out[k * d:k * d + len(cur)] += cur
    return out

def reverse_delay(seg, delay_s, fb=0.55, lp_hz=3000, taps=8):
    e = echo(seg[::-1], delay_s, fb, lp_hz, taps)[::-1]; return e, len(e) - len(seg)

def make_ir(rt60, lp_hz=6000, seed=0):
    r = np.random.default_rng(seed); n = int(rt60 * 1.3 * SR); t = np.arange(n) / SR
    ir = np.stack([r.standard_normal(n), r.standard_normal(n)], axis=1) * (10 ** (-3 * t / rt60))[:, None]
    ir[:, 0] = onepole_lp(ir[:, 0], lp_hz); ir[:, 1] = onepole_lp(ir[:, 1], lp_hz); ir[:int(0.005 * SR)] *= 0.2
    return ir / np.sqrt((ir ** 2).sum(axis=0)).max()

def reverb(st, ir):
    return np.stack([fftconvolve(st[:, 0], ir[:, 0]), fftconvolve(st[:, 1], ir[:, 1])], axis=1)

def saturate(x, drive=1.6):
    return np.tanh(drive * x) / math.tanh(drive)

def place(bus, mono, t, pan, gain=1.0):
    n0 = int(t * SR)
    if n0 >= len(bus) or n0 + len(mono) <= 0: return
    if n0 < 0: mono = mono[-n0:]; n0 = 0
    seg = mono[:len(bus) - n0]; th = (pan + 1) / 2 * math.pi / 2
    bus[n0:n0 + len(seg), 0] += seg * math.cos(th) * gain; bus[n0:n0 + len(seg), 1] += seg * math.sin(th) * gain

# 小星星漂移引擎（取自 render_effects.py）
CTRL_HZ = 200
def coupled_drift(K, n_ctrl, dt, sigma, theta, max_dev, coupling, rng, env=None):
    d = np.zeros((K, n_ctrl)); x = np.zeros(K)
    for k in range(1, n_ctrl):
        e = 1.0 if env is None else env[k]
        x += (-theta * x + coupling * (x.mean() - x)) * dt + sigma * e * math.sqrt(dt) * rng.standard_normal(K)
        x = np.clip(x, -max_dev, max_dev); d[:, k] = x
    return d
def return_to_zero(d, t_ctrl, t_sync, tau):
    d = d.copy(); k0 = np.searchsorted(t_ctrl, t_sync); v0 = d[k0]
    d[k0:] = v0 * np.exp(-(t_ctrl[k0:] - t_sync) / tau); return d
def render_loop_voice(src, rate, resets=(), cf_ms=30):
    pos = np.cumsum(rate) - rate[0]; wins = []
    for n_r in resets:
        c = pos[n_r]; pos[n_r:] -= c; wins.append((n_r, c))
    out = cubic_loop(src, pos); cf = int(cf_ms * SR / 1000)
    for n_r, c in wins:
        n1 = min(n_r + cf, len(pos)); old = cubic_loop(src, pos[n_r:n1] + c); w = np.linspace(0, 1, n1 - n_r)
        out[n_r:n1] = old * (1 - w) + out[n_r:n1] * w
    return out, pos

# ------------------------------------------------------------ 素材
units = json.load(open(os.path.join(SP, "bpmf_units.json")))
speakers = {"阿瑤": dict(file="阿瑤ㄅㄆㄇ.wav", pan=-0.5, cents=+5), "柏豪": dict(file="柏豪ㄅㄆㄇ.wav", pan=0.45, cents=-9), "小軒": dict(file="小軒ㄅㄆㄇ.wav", pan=0.0, cents=-2)}
syl = {}
for name, cfg in speakers.items():
    y = load(cfg["file"]); syl[name] = {}
    for s, (a, b) in units[name].items():
        a = max(0, a - 0.03); b = min(len(y) / SR, b + 0.05)
        syl[name][s] = norm_rms(fade(y[int(a * SR):int(b * SR)]))
words = {}
for name, f, pan in [("阿瑤", "阿瑤朗讀.wav", -0.6), ("柏成", "柏成朗讀.wav", 0.6), ("小軒", "小軒朗讀.wav", 0.1)]:
    y = load(f); iv = librosa.effects.split(y, top_db=30, frame_length=2048, hop_length=512) / SR
    ph = []
    for s, e in iv:
        if ph and s - ph[-1][1] < 0.35: ph[-1][1] = e
        else: ph.append([s, e])
    words[name] = (pan, [norm_rms(fade(y[int(max(0, s - .06) * SR):int((e + .06) * SR)])) for s, e in ph if e - s >= 0.5])
xx = load("中藥行小星星.wav"); XA = fade(xx[int(0.52 * SR):int(19.90 * SR)], 12); LA = len(XA) / SR

dry = np.zeros((N, 2)); echo_bus = np.zeros((N, 2)); hall = np.zeros((N, 2)); blur = np.zeros((N, 2)); bed = np.zeros((N, 2))
cues = []

def say(name, s, t, gain=1.0, fx="dry", pan_jit=0.2, extra_cents=0.0):
    cfg = speakers[name]; seg = syl[name][s]
    cents = cfg["cents"] + extra_cents + wow_curve(len(seg) + 100, 4, 0.4, seed=int(rng.integers(1 << 30)))[:len(seg)]
    seg = vari(seg, cents); pan = float(np.clip(cfg["pan"] + rng.normal(0, pan_jit), -0.9, 0.9))
    if fx == "reverse":
        seg = seg[::-1]
    if fx == "slip":
        n = len(seg); k0 = int(n * 0.45); sl = np.zeros(n); sl[k0:] = -900 * np.linspace(0, 1, n - k0) ** 1.4; seg = vari(seg, sl)
    if fx == "revdelay":
        e, st = reverse_delay(seg, 0.33, fb=0.6, taps=7); place(dry, e, t - st / SR, pan, gain * 0.9); place(hall, e, t - st / SR, pan, gain * 0.4)
    elif fx == "echo":
        place(dry, seg, t, pan, gain); e = echo(seg, 0.29, fb=0.5, lp_hz=2600); place(echo_bus, e, t, -pan * 0.6, gain * 0.7); place(hall, e, t, pan, gain * 0.25)
    else:
        place(dry, seg, t, pan, gain); place(hall, seg, t, pan, gain * 0.2)
    cues.append((round(t, 2), name, s, fx, round(gain, 2)))

# ---- 台灣教學分段：一個人念一整段，段與段之間換人、交錯
GJ = json.load(open(os.path.join(SP, "bpmf_groups.json")))
GROUPS = GJ["order"]
raw = {name: load(cfg["file"]) for name, cfg in speakers.items()}
grp = {}
for name in speakers:
    grp[name] = {}
    for g in GROUPS:
        a0, b0 = GJ["spans"][name][g]
        grp[name][g] = norm_rms(fade(raw[name][int(a0 * SR):int(b0 * SR)], 12))

def say_group(name, g, t, gain=1.0, fx="dry", pan_jit=0.2, extra_cents=0.0):
    if os.environ.get('CLEAN'): fx = 'dry'
    cfg = speakers[name]; seg = grp[name][g]
    cents = cfg["cents"] + extra_cents + wow_curve(len(seg) + 100, 4, 0.3, seed=int(rng.integers(1 << 30)))[:len(seg)]
    seg = vari(seg, cents); pan = float(np.clip(cfg["pan"] + rng.normal(0, pan_jit), -0.9, 0.9))
    if fx == "reverse": seg = seg[::-1]
    if fx == "slip":
        n = len(seg); k0 = int(n * 0.55); sl = np.zeros(n); sl[k0:] = -900 * np.linspace(0, 1, n - k0) ** 1.4; seg = vari(seg, sl)
    if fx == "revdelay":
        e, st = reverse_delay(seg, 0.36, fb=0.6, taps=7); place(dry, e, t - st / SR, pan, gain * 0.9); place(hall, e, t - st / SR, pan, gain * 0.4)
    elif fx == "echo":
        place(dry, seg, t, pan, gain); e = echo(seg, 0.31, fb=0.5, lp_hz=2600); place(echo_bus, e, t, -pan * 0.6, gain * 0.7); place(hall, e, t, pan, gain * 0.25)
    else:
        place(dry, seg, t, pan, gain); place(hall, seg, t, pan, gain * 0.2)
    cues.append((round(t, 2), name, g, fx, round(gain, 2), round(len(seg) / SR, 2)))
    return len(seg) / SR

def dur_of(name, g): return len(grp[name][g]) / SR

# 1. ㄅㄆㄇㄈ：阿瑤先念，柏豪在她念到一半接進來，小軒再接；然後三人同念一次但相位錯開
t = 0.6
d = say_group("阿瑤", GROUPS[0], t)
d2 = say_group("柏豪", GROUPS[0], t + d * 0.55, gain=0.9)
d3 = say_group("小軒", GROUPS[0], t + d * 0.55 + d2 * 0.5, gain=0.85)
t = t + d * 0.55 + d2 * 0.5 + d3 + 0.5
for k, name in enumerate(["阿瑤", "柏豪", "小軒"]):
    say_group(name, GROUPS[0], t + k * 0.12, gain=0.7, fx="echo" if k == 2 else "dry")
t += max(dur_of(n, GROUPS[0]) for n in speakers) + 0.6

# 2. ㄉㄊㄋㄌ 到 ㄐㄑㄒ：輪流一人念一段，下一位在段尾前就接上（此起彼落），偶爾回應同一段
order = ["柏豪", "阿瑤", "小軒"]
for gi in range(1, 4):
    sp = order[gi % 3]; nxt = order[(gi + 1) % 3]
    d = say_group(sp, GROUPS[gi], t)
    if gi >= 2:
        say_group(nxt, GROUPS[gi], t + d * 0.45, gain=0.6, fx="echo" if gi == 3 else "dry")
    t += d * np.interp(gi, [1, 3], [0.95, 0.7])

# 3. ㄓㄔㄕㄖ 到 ㄚㄛㄜㄝ：三人同念同一段，相位逐段拉開；穿插 reverse delay 與整段反轉
for gi in range(4, 8):
    off = 0.15 + (gi - 4) * 0.18
    ds = []
    for k, name in enumerate(["阿瑤", "柏豪", "小軒"]):
        fx = "revdelay" if (gi == 5 and k == 1) else ("reverse" if (gi == 7 and k == 2) else "dry")
        ds.append(say_group(name, GROUPS[gi], t + k * off, gain=0.8, fx=fx))
    t += max(ds) + 2 * off - np.interp(gi, [4, 7], [0.6, 0.2])

# 4. ㄞㄟㄠㄡ、ㄢㄣㄤㄥ、ㄦ：漸慢、散開、slip；ㄦ 三人各一次再反轉回聲收尾
for gi in range(8, 11):
    off = 0.6 + (gi - 8) * 0.35
    ds = []
    for k, name in enumerate(["阿瑤", "柏豪", "小軒"]):
        fx = "slip" if (gi == 9 and k == 1) else ("echo" if gi == 10 else "dry")
        ds.append(say_group(name, GROUPS[gi], t + k * off, gain=0.75 - (gi - 8) * 0.08, fx=fx))
    t += max(ds) + 2 * off + np.interp(gi, [8, 10], [0.4, 1.2])
t_end_seq = t
for k, name in enumerate(["阿瑤", "柏豪", "小軒"]):
    say_group(name, GROUPS[10], t_end_seq + 0.8 + k * 1.1, gain=0.5, fx="reverse")   # 以最後一段 ㄧㄨㄩ 反轉收尾

# ---- 「ㄅㄆㄇㄈ」四聲部 phase loop 低聲墊底（18–52 s）
bp = np.concatenate([syl["柏豪"][s] for s in SYM[:4]]); bp = fade(bp, 12)
for i, c in enumerate([0, 6, -6, 12]):
    n_loop = int(40 * SR); src = np.tile(bp, int(np.ceil(n_loop / len(bp))) + 1)
    seg = vari(src, c + wow_curve(len(src), 3, 0.2, seed=300 + i))[:n_loop]
    env = np.ones(n_loop); a = int(10 * SR); d = int(12 * SR); env[:a] = np.linspace(0, 1, a); env[-d:] = np.linspace(1, 0, d)
    seg = onepole_lp(seg * env, 3000) * 0.22
    place(dry, seg, 18, [-0.7, -0.25, 0.25, 0.7][i]); place(hall, seg, 18, [-0.7, -0.25, 0.25, 0.7][i], 0.6)

# ---- 單詞模糊墊底（14–74 s）：慢 300 cents、低通 1.6 kHz、大殘響、部分反轉
tw = 14.0
while tw < 80:
    name = rng.choice(list(words)); pan, ph = words[name]; seg = ph[int(rng.integers(len(ph)))]
    seg = vari(seg, -300 + wow_curve(len(seg) * 2, 12, 0.3, seed=int(rng.integers(1 << 30)))[:len(seg)])
    if rng.random() < 0.4: seg = seg[::-1]
    seg = onepole_lp(onepole_lp(seg, 1600), 1600)
    g = 0.35 * np.interp(tw, [14, 30, 66, 80], [0.3, 1.0, 1.0, 0.2])
    place(blur, seg, tw, float(np.clip(pan + rng.normal(0, 0.3), -0.9, 0.9)), g)
    cues.append((round(tw, 2), name + "朗讀", "詞", "blur", round(g, 2)))
    tw += rng.uniform(1.6, 4.0)

# ---- 小星星尾聲（52–100 s）：三聲部耦合漂移，84 s SYNC，下一個半句邊界對齊
bed_start = 52.0; n_bed = N - int(bed_start * SR)
n_ctrl = int(n_bed / SR * CTRL_HZ) + 2; t_ctrl = np.arange(n_ctrl) / CTRL_HZ
env = np.clip((t_ctrl - 4) / 22, 0, 1)
D = coupled_drift(3, n_ctrl, 1 / CTRL_HZ, sigma=7.0, theta=0.03, max_dev=16, coupling=0.5, rng=np.random.default_rng(3), env=env)
t_sync_rel = 78.0 - bed_start; tau = 2.5
grid = LA / 2; n_r = int(round(math.ceil((t_sync_rel + 3 * tau) / grid) * grid * SR)); assert n_r < n_bed - SR, "reset 超出尾聲長度"
bed_voices = []; poss = []
for i, (rate0, pan, gain, lp) in enumerate([(0.5, 0.0, 0.95, 2200), (1.0, -0.55, 0.5, 2600), (1.0, 0.55, 0.5, 2600)]):
    d = return_to_zero(D[i], t_ctrl, t_sync_rel, tau)
    rate = rate0 * 2 ** (np.interp(np.arange(n_bed) / SR, t_ctrl, d) / 1200)
    v, p = render_loop_voice(XA, rate, resets=[n_r]); poss.append(p)
    v = onepole_lp(onepole_lp(v, lp), lp)
    fe = np.ones(n_bed); a = int(16 * SR); fo = int(7 * SR); fe[:a] = np.linspace(0, 1, a) ** 2; fe[-fo:] = np.linspace(1, 0, fo)
    place(bed, v * fe * gain, bed_start, pan)
bed_lag = [(poss[k][n_r - 10] - poss[0][n_r - 10]) / SR * 1000 for k in (1, 2)], [(poss[k][n_r + 4800] - poss[0][n_r + 4800]) / SR * 1000 for k in (1, 2)]

# ------------------------------------------------------------ 混音
room = make_ir(0.7, lp_hz=5000, seed=1); big = make_ir(4.2, lp_hz=3200, seed=2)
if os.environ.get('STEMS'):
    sd = os.path.join(OUT, "03_素材層"); os.makedirs(sd, exist_ok=True)
    def _w(fn, x, note):
        x = x[:N]; pk = np.abs(x).max(); x = x / pk * 10 ** (-1 / 20) if pk > 10 ** (-1 / 20) else x
        sf.write(os.path.join(sd, fn), x, SR, subtype="PCM_24"); print("stem", fn, note)
    tag = "乾淨版" if os.environ.get('CLEAN') else "效果版"
    _w(f"注音_三人依序分段交錯_{tag}_0-48s.wav", saturate(dry, 1.6) + echo_bus * 0.9 + reverb(saturate(dry, 1.6) + echo_bus * 0.9, room)[:N] * 0.22 + reverb(hall, big)[:N] * 0.5,
       "三人依台灣教學分段交錯，含 ㄅㄆㄇㄈ phase loop 墊底" + ("，無任何效果（只有 detune、小房間殘響）" if os.environ.get('CLEAN') else "，含 tape echo、reverse delay、反轉、slip"))
    if not os.environ.get('CLEAN'):
        _w("朗讀單詞_模糊墊底層_14-80s.wav", saturate(blur * 0.5 + reverb(blur, big)[:N] * 0.9, 1.3), "飛翔、媽媽等單詞：慢 300 cents、低通 1.6 kHz、大殘響、四成反轉")
        _w("小星星_三聲部耦合漂移_78s重同步_52-100s.wav", saturate(bed * 0.7 + reverb(bed, big)[:N] * 0.6, 1.3) * 0.9, "低八度慢速＋兩個原速聲部，低通、大殘響，78 s SYNC、90.8 s 對齊")
    if not os.environ.get('MIX'): raise SystemExit(0)
sp = saturate(dry, 1.6) + echo_bus * 0.9
mix = sp + reverb(sp, room)[:N] * 0.22 + reverb(hall, big)[:N] * 0.5
mix += saturate(blur * 0.5 + reverb(blur, big)[:N] * 0.9, 1.3)
mix += saturate(bed * 0.7 + reverb(bed, big)[:N] * 0.6, 1.3) * 0.9
hiss = np.stack([onepole_lp(rng.standard_normal(N), 4000), onepole_lp(rng.standard_normal(N), 4000)], axis=1)
mix += hiss * np.clip((np.arange(N) / SR - 40) / 20, 0, 1)[:, None] * 10 ** (-58 / 20)
fo = int(6 * SR); mix[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.5; mix[:480] *= np.linspace(0, 1, 480)[:, None]
mix = np.tanh(mix * 1.2) / math.tanh(1.2); mix /= np.abs(mix).max() / 10 ** (-1 / 20)
name = "12_注音依序交錯_小星星尾聲_v2.wav"
sf.write(os.path.join(OUT, name), mix, SR, subtype="PCM_24")
json.dump(cues, open(os.path.join(OUT, "12_cue_sheet.json"), "w"), ensure_ascii=False, indent=0)
print("wrote", name, f"{N/SR:.0f}s cues {len(cues)} seq_end {t_end_seq:.1f}s bed reset at {bed_start + n_r/SR:.1f}s  lag before/after reset (ms): {np.round(bed_lag[0])} / {np.round(bed_lag[1])}")

# ------------------------------------------------------------ 時間軸圖
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt; from matplotlib import font_manager
import glob
_c = [f for f in ["/System/Library/Fonts/PingFang.ttc", "/System/Library/Fonts/Hiragino Sans GB.ttc", "/System/Library/Fonts/STHeiti Light.ttc", "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"] + glob.glob("/System/Library/Fonts/*Hiragino*") if os.path.exists(f)]
fp = font_manager.FontProperties(fname=_c[0]) if _c else None
fig, ax = plt.subplots(2, 1, figsize=(16, 6), sharex=True, gridspec_kw=dict(height_ratios=[3, 1]))
rows = ["阿瑤", "柏豪", "小軒", "阿瑤朗讀", "柏成朗讀", "小軒朗讀"]
col = dict(dry="#555", echo="#1f77b4", revdelay="#2ca02c", reverse="#d62728", slip="#ff7f0e", blur="#9467bd")
for c in cues:
    tt, who, s, fx, g = c[:5]; ln = c[5] if len(c) > 5 else 2.0
    y0 = rows.index(who); ax[0].barh(y0, ln, left=tt, height=0.6, color=col[fx], alpha=0.75)
    if who in speakers: ax[0].text(tt, y0 + 0.33, s, fontproperties=fp, fontsize=6)
ax[0].set_yticks(range(len(rows))); ax[0].set_yticklabels(rows, fontproperties=fp)
ax[0].axvspan(18, 52, color="orange", alpha=0.07); ax[0].axvspan(52, DUR, color="purple", alpha=0.08)
ax[0].text(19, 5.6, "ㄅㄆㄇㄈ phase loop", fontproperties=fp, fontsize=9); ax[0].text(70, 5.6, "小星星耦合漂移 → 78 s SYNC", fontproperties=fp, fontsize=9)
ax[0].set_title("12 v2 時間軸：灰 dry、藍 echo、綠 reverse delay、紅反轉、橘 slip、紫 模糊單詞", fontproperties=fp)
rms = librosa.feature.rms(y=mix.mean(axis=1), frame_length=4800, hop_length=2400)[0]
ax[1].plot(np.arange(len(rms)) * 2400 / SR, 20 * np.log10(rms + 1e-9)); ax[1].set_ylabel("dBFS"); ax[1].set_xlabel("s"); ax[1].grid(alpha=.3)
fig.tight_layout(); fig.savefig(os.path.join(OUT, "12_時間軸.png"), dpi=80)
