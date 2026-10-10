#!/usr/bin/env python
"""
《節奏繞纏》呼吸素材 四軌盤帶具象拼貼
給 Dicy2 memory 用，也可單獨當聲音素材。

素材：錄音/Splice素材/ 的呼吸類（排除口腔吞嚥），已 loudnorm 到 -20 LUFS 的中繼檔
效果：varispeed wow/flutter、磁帶飽和、磁頭高頻衰減、軌間串音、reverse delay、FDN 空間

varispeed 與 OU 漂移的做法沿用 錄音/效果測試_20260902/scripts/render_effects.py，
cubic_read 與 ou_drift 為該腳本的同源實作。
"""
import os, math
import numpy as np
import soundfile as sf

SR = 44100
WORK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dicy2_work")
OUT = os.path.expanduser(
    "~/Library/Mobile Documents/com~apple~CloudDocs/Documents/03_Projects_Operations/"
    "Active/ITRI_工研院藝術進駐/錄音/Dicy2_memory")
DUR = 160.0                      # 總長 2:40
N = int(DUR * SR)
rng = np.random.default_rng(20260907)

# ---------------------------------------------------------------- 基礎工具

def load(stem):
    """依檔名片段從中繼檔載入（已 44.1k / mono / -20 LUFS）。"""
    for f in sorted(os.listdir(WORK)):
        if stem in f and f.endswith(".wav"):
            y, sr = sf.read(os.path.join(WORK, f), always_2d=True)
            assert sr == SR, f"{f} sr={sr}"
            return y.mean(axis=1).astype(np.float64)
    raise FileNotFoundError(stem)

def cubic_read(src, pos):
    """4 點 Catmull-Rom 內插，pos 以 sample 為單位，自動 wrap。"""
    L = len(src)
    pos = np.mod(pos, L)
    i1 = np.floor(pos).astype(np.int64)
    f = pos - i1
    i0 = (i1 - 1) % L; i2 = (i1 + 1) % L; i3 = (i1 + 2) % L
    p0, p1, p2, p3 = src[i0], src[i1], src[i2], src[i3]
    return p1 + 0.5 * f * (p2 - p0 + f * (2*p0 - 5*p1 + 4*p2 - p3 + f * (3*(p1-p2) + p3 - p0)))

def ou_drift(n_ctrl, dt, sigma_cents, theta, max_dev, rng):
    """Ornstein-Uhlenbeck random walk（cents），有均值回歸與上限。"""
    d = np.zeros(n_ctrl); x = 0.0
    for k in range(1, n_ctrl):
        x += -theta * x * dt + sigma_cents * math.sqrt(dt) * rng.standard_normal()
        x = max(-max_dev, min(max_dev, x))
        d[k] = x
    return d

def tape_rate(n, wow_cents, wow_theta, flutter_hz, flutter_cents, rng):
    """盤帶速率曲線：慢速 wow（OU）＋ 固定頻率 flutter。"""
    ctrl_hz = 100.0
    n_ctrl = int(n / SR * ctrl_hz) + 2
    t_ctrl = np.arange(n_ctrl) / ctrl_hz
    wow = ou_drift(n_ctrl, 1.0/ctrl_hz, wow_cents, wow_theta, wow_cents*2.5, rng)
    t = np.arange(n) / SR
    cents = np.interp(t, t_ctrl, wow)
    cents += flutter_cents * np.sin(2*np.pi*flutter_hz*t + rng.uniform(0, 6.28))
    return 2.0 ** (cents / 1200.0)

def varispeed(src, n, rate, pos0=0.0):
    pos = np.cumsum(rate) - rate[0] + pos0
    return cubic_read(src, pos)

def saturate(x, drive):
    """磁帶軟飽和。drive 越大越壓。"""
    return np.tanh(x * drive) / np.tanh(drive)

def onepole_lp(x, fc):
    """磁頭高頻衰減。"""
    a = math.exp(-2*math.pi*fc/SR)
    y = np.empty_like(x); z = 0.0
    for i in range(len(x)):
        z = (1-a)*x[i] + a*z
        y[i] = z
    return y

def onepole_lp_fast(x, fc):
    """一階低通的向量化近似（用 lfilter 等價的遞迴，改以 IIR 展開避免 python loop）。"""
    from math import exp, pi
    a = exp(-2*pi*fc/SR)
    # 以指數衰減核做 FFT 卷積，長度截到 -60 dB
    L = int(min(len(x), max(16, -6.9078 / math.log(a) if a > 0 else 16)))
    k = (1-a) * a ** np.arange(L)
    nfft = 1 << int(np.ceil(np.log2(len(x) + L)))
    y = np.fft.irfft(np.fft.rfft(x, nfft) * np.fft.rfft(k, nfft), nfft)[:len(x)]
    return y

def place(dst, src, t0, gain=1.0, fade=0.05):
    """把一段素材放進時間軸，頭尾各帶淡入淡出，避免邊界不連續。"""
    n0 = int(t0 * SR)
    seg = src.copy() * gain
    nf = int(fade * SR)
    if len(seg) > 2*nf:
        w = np.linspace(0, 1, nf)
        seg[:nf] *= w; seg[-nf:] *= w[::-1]
    n1 = min(n0 + len(seg), len(dst))
    dst[n0:n1] += seg[:n1-n0]

def reverse_delay(x, delay_s, chunk_s, fb, mix):
    """把訊號切成 chunk、每塊反轉後延遲送出，帶回授。經典 reverse delay。"""
    out = np.zeros(len(x) + int(delay_s*SR) + int(chunk_s*SR))
    ch = int(chunk_s * SR)
    dl = int(delay_s * SR)
    w = np.hanning(ch)
    g = mix
    for rep in range(4):                       # 回授以四次重複近似
        if g < 0.01: break
        off = dl * (rep + 1)
        for n0 in range(0, len(x) - ch, ch // 2):
            seg = x[n0:n0+ch] * w
            p = n0 + off
            if p + ch < len(out):
                out[p:p+ch] += seg[::-1] * g
        g *= fb
    return out[:len(x)]

def fdn_reverb(x, rt60, mix, size=1.0):
    """4 線 feedback delay network，Hadamard 混合矩陣。"""
    delays = [int(d*size) for d in (1931, 2467, 3121, 3739)]
    g = [10 ** (-3.0 * d / SR / rt60) for d in delays]
    bufs = [np.zeros(d) for d in delays]
    idx = [0]*4
    out = np.zeros(len(x))
    damp = 0.35
    z = [0.0]*4
    H = 0.5 * np.array([[1,1,1,1],[1,-1,1,-1],[1,1,-1,-1],[1,-1,-1,1]], dtype=np.float64)
    for i in range(len(x)):
        r = np.array([bufs[k][idx[k]] for k in range(4)])
        for k in range(4):                      # 每線低通模擬空氣吸收
            z[k] = (1-damp)*r[k] + damp*z[k]
            r[k] = z[k]
        s = H @ r
        for k in range(4):
            bufs[k][idx[k]] = x[i] + s[k] * g[k]
            idx[k] = (idx[k] + 1) % delays[k]
        out[i] = r.sum() * 0.25
    return x * (1-mix) + out * mix

def fdn_reverb_fast(x, rt60, mix, size=1.0):
    """把 FDN 的脈衝響應算出來再做 FFT 卷積，避免逐 sample 的 python 迴圈。"""
    ir_len = int(rt60 * 1.5 * SR)
    imp = np.zeros(ir_len); imp[0] = 1.0
    ir = fdn_reverb(imp, rt60, 1.0, size)
    nfft = 1 << int(np.ceil(np.log2(len(x) + ir_len)))
    wet = np.fft.irfft(np.fft.rfft(x, nfft) * np.fft.rfft(ir, nfft), nfft)[:len(x)]
    wet /= (np.max(np.abs(wet)) + 1e-12)
    wet *= np.max(np.abs(x))
    return x * (1-mix) + wet * mix

# ---------------------------------------------------------------- 素材

print("載入素材")
M = {
    "mask":      load("BRS_Human_F_Breaths_Mask_1"),
    "deep_f":    load("BRS_Human_Breaths_Female_Deep_02"),
    "scared":    load("BRS_Human_Breaths_Male_Scared"),
    "cool3":     load("BRS_Human_F_Breaths_Exercise_Cool_Down_3"),
    "cool4":     load("BRS_Human_F_Breaths_Exercise_Cool_Down_4"),
    "steady":    load("BRS_Human_F_Breaths_Exercise_Steady.wav"),
    "steadyslow":load("BRS_Human_F_Breaths_Exercise_Steady-Slow_3"),
    "candles":   load("BRS_Human_Breath_Exhale_Blow_Out_Candles"),
    "gulps":     load("BRS_Voice_Male_Breaths_Inhale_Gulps"),
    "forest_h":  load("EX_RE_vocal_cilaos_forest_heavy"),
    "forest_r":  load("EX_RE_vocal_cilaos_forest_rhythmic"),
    "group":     load("EX_BR_FX_Group_Vocals_One_Breath"),
    "whisper":   load("EX_BR_FX_Sa_Whisper"),
    "wheeze":    load("BreatheWheeze_BW"),
    "wheezelong":load("BreathWheezeLong"),
    "snore":     load("SnoreSleep"),
    "baby_sigh": load("BRS_Baby_6_Month_Old_Breaths_Sigh"),
    "baby_yawn": load("BRS_Baby_6_Month_Old_Breaths_Yawn"),
    "nose":      load("EX_BR_Vocal_FX_Nose_Out"),
    "gasp":      load("EX_BR_Vocal_FX_Gasp_Deep"),
    "sharon1":   load("ESM_Character_Sharon_Breathing_1"),
    "sigh_m":    load("ESM_GCAW_vocals_breath_male_deep_sigh"),
    "exhale_calm": load("EX_BR_Vocal_FX_Exhale_Calm_Male_Dry"),
    "shh":       load("EX_BR_Vocal_FX_Shh_Exhale"),
    "ai_breath": load("EX_AI_90_vocal_breath_dry"),
}
for k, v in M.items():
    print(f"  {k:12s} {len(v)/SR:6.2f}s")

# ---------------------------------------------------------------- 四軌配置
# 形式：稀疏 → 疊加 → 最密 → 退去 → 純淨收尾
# 每軌先鋪素材（少量切點、長段為主），之後整軌過盤帶處理

T = [np.zeros(N) for _ in range(4)]

# 軌 1：底層。長段連續呼吸，慢速鋪底，全曲不斷
place(T[0], M["mask"],        0.0,  0.85, fade=3.0)
place(T[0], M["deep_f"],     48.0,  0.80, fade=2.0)
place(T[0], M["mask"][int(20*SR):], 78.0, 0.70, fade=2.5)
place(T[0], M["scared"],     108.0, 0.45, fade=3.0)

# 軌 2：運動緩和呼吸。中段進入，是全曲的節奏骨幹
place(T[1], M["cool4"],       26.0, 0.75)
place(T[1], M["steadyslow"],  36.0, 0.80)
place(T[1], M["cool3"],       48.5, 0.85)
place(T[1], M["steady"],      61.0, 0.80)
place(T[1], M["cool3"],       68.0, 0.75)
place(T[1], M["steadyslow"],  80.5, 0.85)
place(T[1], M["cool4"],       92.0, 0.70)
place(T[1], M["cool3"],      101.0, 0.55)

# 軌 3：實地錄音與群體呼吸。空間最深的一軌
place(T[2], M["forest_h"],    14.0, 0.65)
place(T[2], M["whisper"],     33.0, 0.55)
place(T[2], M["forest_r"],    44.0, 0.70)
place(T[2], M["group"],       57.0, 0.75)
place(T[2], M["forest_h"],    74.0, 0.60)
place(T[2], M["group"],       86.0, 0.80)
place(T[2], M["ai_breath"],  100.0, 0.60)
place(T[2], M["forest_r"],   112.0, 0.50)

# 軌 4：點狀與病理。稀疏的前景事件
place(T[3], M["gasp"],         8.5, 0.55)
place(T[3], M["nose"],        21.0, 0.50)
place(T[3], M["baby_sigh"],   31.0, 0.45)
place(T[3], M["wheeze"],      41.0, 0.55)
place(T[3], M["gulps"],       53.0, 0.60)
place(T[3], M["baby_yawn"],   64.0, 0.50)
place(T[3], M["wheezelong"],  71.0, 0.60)
place(T[3], M["snore"],       88.0, 0.55)
place(T[3], M["candles"],     97.0, 0.65)
place(T[3], M["sharon1"],    110.0, 0.50)
place(T[3], M["sigh_m"],     118.0, 0.55)
place(T[3], M["shh"],        124.0, 0.45)

# ---------------------------------------------------------------- 盤帶處理
# 每軌不同的 wow/flutter 深度與磁頭特性，模擬四軌機各軌走帶狀態不同

print("盤帶處理")
TAPE = [
    # wow_cents, wow_theta, flutter_hz, flutter_cents, drive, head_fc
    (14.0, 0.35, 6.2,  2.2, 1.4,  7200),   # 軌1 底層：漂移最深、最悶
    ( 8.0, 0.55, 7.8,  1.4, 1.8,  9000),   # 軌2 骨幹：穩一些
    (11.0, 0.40, 5.4,  1.9, 1.2,  6200),   # 軌3 空間：悶且飄
    ( 6.0, 0.70, 9.1,  1.1, 2.2, 11000),   # 軌4 前景：最穩最亮
]
for k in range(4):
    wc, wt, fh, fc_, drive, head = TAPE[k]
    rate = tape_rate(N, wc, wt, fh, fc_, rng)
    T[k] = varispeed(T[k], N, rate)
    T[k] = saturate(T[k], drive)
    T[k] = onepole_lp_fast(T[k], head)
    print(f"  軌{k+1} wow±{wc:.0f}c flutter {fh}Hz drive {drive} head {head}Hz")

# 軌間串音：四軌機相鄰磁軌會互相滲，帶 1.2 ms 延遲
print("軌間串音")
xt = int(0.0012 * SR)
orig = [t.copy() for t in T]
for k in range(4):
    for j in (k-1, k+1):
        if 0 <= j < 4:
            T[k][xt:] += orig[j][:-xt] * 0.045

# ---------------------------------------------------------------- 空間與 reverse delay

print("reverse delay")
# 軌 3 送最多（空間軌），軌 1 少量，其餘不送
rd = np.zeros(N)
rd += reverse_delay(T[2], delay_s=0.62, chunk_s=1.4, fb=0.45, mix=0.55)
rd += reverse_delay(T[0], delay_s=1.10, chunk_s=2.2, fb=0.38, mix=0.30)
rd += reverse_delay(T[3], delay_s=0.38, chunk_s=0.9, fb=0.30, mix=0.22)

print("FDN 空間（算脈衝響應）")
dry = sum(T)
send = T[2]*0.65 + T[0]*0.35 + T[1]*0.25 + T[3]*0.20 + rd*0.5
wet_long  = fdn_reverb_fast(send, rt60=4.2, mix=1.0, size=1.0)
wet_short = fdn_reverb_fast(dry,  rt60=1.1, mix=1.0, size=0.55)

# ---------------------------------------------------------------- 混音
# 空間量隨曲子起伏：中段最濕，尾段收乾
t = np.arange(N) / SR
wet_env = np.interp(t, [0, 20, 60, 100, 128, 140, 160],
                       [0.35, 0.5, 0.75, 0.8, 0.5, 0.12, 0.05])
rd_env  = np.interp(t, [0, 25, 55, 95, 125, 138, 160],
                       [0.0, 0.15, 0.55, 0.6, 0.35, 0.05, 0.0])

mono = dry * 0.75 + wet_long * wet_env * 0.55 + wet_short * 0.18 + rd * rd_env * 0.5

# 尾聲：一段完全乾淨、沒有任何處理的深吐氣，呼應素材本來的樣子
tail = np.zeros(N)
place(tail, M["exhale_calm"], 143.0, 0.9, fade=0.4)
mono = mono + tail

# 立體聲：四軌各自定位，reverse delay 展寬
pans = [0.42, 0.58, 0.18, 0.80]          # 0 左 1 右
L = np.zeros(N); R = np.zeros(N)
for k in range(4):
    p = pans[k]
    L += T[k] * math.cos(p * math.pi/2)
    R += T[k] * math.sin(p * math.pi/2)
L = L*0.75 + wet_long*wet_env*0.5 + wet_short*0.16 + np.roll(rd, 220)*rd_env*0.45 + tail*0.9
R = R*0.75 + np.roll(wet_long, 330)*wet_env*0.5 + wet_short*0.16 + rd*rd_env*0.45 + tail*0.9

# ---------------------------------------------------------------- 輸出

def norm(x, peak_db=-1.0):
    p = np.max(np.abs(x))
    return x * (10 ** (peak_db/20.0) / p)

os.makedirs(OUT, exist_ok=True)
mono_n = norm(mono)
st = np.stack([norm(L), norm(R)], axis=1)
# 立體聲兩聲道要用同一增益，否則影像會歪
g = 10 ** (-1.0/20.0) / max(np.max(np.abs(L)), np.max(np.abs(R)))
st = np.stack([L*g, R*g], axis=1)

sf.write(os.path.join(OUT, "dicy2_memory_C_呼吸盤帶拼貼_mono.wav"), mono_n, SR, subtype="PCM_24")
sf.write(os.path.join(OUT, "呼吸盤帶拼貼_stereo.wav"), st, SR, subtype="PCM_24")

d = np.abs(np.diff(mono_n))
print()
print(f"總長 {DUR:.0f}s")
print(f"mono peak {20*math.log10(np.max(np.abs(mono_n))):.2f} dBFS  RMS {20*math.log10(np.sqrt((mono_n**2).mean())):.1f} dBFS")
print(f"stereo peak {20*math.log10(np.max(np.abs(st))):.2f} dBFS")
print(f"不連續檢查：最大單樣本躍變 {np.max(d):.4f}，超過 0.15 的點 {(d>0.15).sum()} 個")
