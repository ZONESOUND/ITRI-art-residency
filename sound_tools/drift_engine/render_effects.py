#!/usr/bin/env python
"""
《節奏繞纏》離線效果示範 render 腳本
素材：中藥行小星星.wav（44.1k）、柏豪／阿瑤／小軒 ㄅㄆㄇ.wav（48k）
輸出：錄音/效果測試_20260902/*.wav（24-bit）＋ README.md
所有效果都是 varispeed（速度與音高綁定）除了 04 的 pitch-only detune。
"""
import os, sys, json, math
import numpy as np
import soundfile as sf
import librosa

SRC = os.path.expanduser(
    "~/Library/Mobile Documents/com~apple~CloudDocs/Documents/03_Projects_Operations/Active/ITRI_工研院藝術進駐/錄音")
OUT = os.path.join(SRC, "效果測試_20260902")
os.makedirs(OUT, exist_ok=True)
REPORT = []          # (檔名, 秒數, peak dBFS, 備註)
LAGCHECK = []        # 聲部間時間差（由播放位置精確計算）
CLICKS = []          # 不連續樣本計數

# ---------------------------------------------------------------- 基礎工具
def load_mono(name):
    y, sr = sf.read(os.path.join(SRC, name), always_2d=True)
    return y.mean(axis=1).astype(np.float64), sr

def cut(y, sr, t0, t1, fade=0.012):
    seg = y[int(round(t0 * sr)):int(round(t1 * sr))].copy()
    n = int(fade * sr)
    w = np.linspace(0, 1, n)
    seg[:n] *= w
    seg[-n:] *= w[::-1]
    return seg

def cubic_read(src, pos):
    """4 點 Catmull-Rom 內插，pos 以 sample 為單位，自動 wrap（loop）。"""
    L = len(src)
    pos = np.mod(pos, L)
    i1 = np.floor(pos).astype(np.int64)
    f = pos - i1
    i0 = (i1 - 1) % L
    i2 = (i1 + 1) % L
    i3 = (i1 + 2) % L
    p0, p1, p2, p3 = src[i0], src[i1], src[i2], src[i3]
    return p1 + 0.5 * f * (p2 - p0 + f * (2 * p0 - 5 * p1 + 4 * p2 - p3 + f * (3 * (p1 - p2) + p3 - p0)))

def ou_drift(n_ctrl, dt, sigma_cents, theta, max_dev, rng, env=None):
    """Ornstein-Uhlenbeck random walk（cents），有均值回歸與上限。"""
    d = np.zeros(n_ctrl)
    x = 0.0
    for k in range(1, n_ctrl):
        e = 1.0 if env is None else env[k]
        x += -theta * x * dt + sigma_cents * e * math.sqrt(dt) * rng.standard_normal()
        x = max(-max_dev, min(max_dev, x))
        d[k] = x
    return d

def coupled_drift(K, n_ctrl, dt, sigma_cents, theta, max_dev, coupling, rng, env=None):
    """K 個聲部的 OU 漂移，加上把各聲部拉向平均值的耦合項。"""
    d = np.zeros((K, n_ctrl))
    x = np.zeros(K)
    for k in range(1, n_ctrl):
        e = 1.0 if env is None else env[k]
        noise = sigma_cents * e * math.sqrt(dt) * rng.standard_normal(K)
        mean = x.mean()
        x += (-theta * x + coupling * (mean - x)) * dt + noise
        x = np.clip(x, -max_dev, max_dev)
        d[:, k] = x
    return d

def return_to_zero(d_ctrl, t_ctrl, t_sync, tau):
    """從 t_sync 起，cents 偏移以時間常數 tau 指數衰減回 0（RETURN SPEED）。"""
    d = d_ctrl.copy()
    k0 = np.searchsorted(t_ctrl, t_sync)
    start_val = d[k0]
    for k in range(k0, len(d)):
        d[k] = start_val * math.exp(-(t_ctrl[k] - t_sync) / tau)
    return d

def cents_to_rate(c):
    return 2.0 ** (c / 1200.0)

def to_audio_rate(ctrl, t_ctrl, n_out, sr):
    t = np.arange(n_out) / sr
    return np.interp(t, t_ctrl, ctrl)

def render_voice(src, rate, resets=(), pos0=0.0, cf_ms=30, sr=44100, pos_override=None, amp=None):
    """
    rate: 每個輸出 sample 的播放速率（1.0 = 原速）
    resets: [(sample_index)] 在這些時間點把播放位置硬拉回 loop 起點（帶 crossfade）
    pos_override: [(n0, n1, pos_array)] 直接覆蓋某段的播放位置（stutter 用）
    """
    pos = np.cumsum(rate) - rate[0] + pos0
    out = None
    if pos_override:
        for n0, n1, p in pos_override:
            pos[n0:n1] = p
    cf = int(cf_ms * sr / 1000)
    windows = []
    for n_r in resets:
        c = pos[n_r]
        pos[n_r:] -= c
        windows.append((n_r, c))
    out = cubic_read(src, pos)
    for n_r, c in windows:  # crossfade 舊位置 → 新位置
        n1 = min(n_r + cf, len(pos))
        old = cubic_read(src, pos[n_r:n1] + c)
        w = np.linspace(0, 1, n1 - n_r)
        out[n_r:n1] = old * (1 - w) + out[n_r:n1] * w
    if amp is not None:
        out *= amp
    return out, pos


def finish(tag, voices, poss, sr, check_times, cents_curves=None, t_ctrl=None, loop_len=None):
    """證據：用播放位置差算精確的聲部時間差、檢查不連續（click）、畫偏移曲線圖。"""
    for tt in check_times:
        n = min(int(tt * sr), len(poss[0]) - 1)
        LAGCHECK.append((tag, round(float(tt), 1), [round((poss[k][n] - poss[0][n]) / sr * 1000) for k in range(1, len(poss))]))
    mix = sum(voices)
    d = np.abs(np.diff(mix))
    CLICKS.append((tag, int((d > 0.25 * np.abs(mix).max()).sum())))
    if cents_curves is not None:
        import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
        fig, ax = plt.subplots(2, 1, figsize=(14, 6), sharex=True)
        for i, c in enumerate(cents_curves):
            ax[0].plot(t_ctrl, c, lw=1, label=f"voice {i+1}")
        ax[0].set_ylabel("offset (cents)"); ax[0].legend(loc="upper left", fontsize=8); ax[0].grid(alpha=.3)
        step = max(1, sr // 50)
        tt = np.arange(0, len(poss[0]), step) / sr
        for k in range(1, len(poss)):
            ax[1].plot(tt, (poss[k][::step] - poss[0][::step]) / sr * 1000, lw=1, label=f"voice {k+1} vs 1")
        if loop_len:
            for g in np.arange(0, tt[-1], loop_len): ax[1].axvline(g, color="k", alpha=.15)
        ax[1].set_ylabel("timing offset (ms)"); ax[1].set_xlabel("s"); ax[1].grid(alpha=.3); ax[1].legend(loc="upper left", fontsize=8)
        fig.suptitle(tag); fig.tight_layout()
        fig.savefig(os.path.join(OUT, f"曲線_{tag}.png"), dpi=80); plt.close(fig)

def pan_mix(voices, pans, sr, tail_fade=2.0):
    n = max(len(v) for v in voices)
    L = np.zeros(n); R = np.zeros(n)
    for v, p in zip(voices, pans):
        th = (p + 1) / 2 * math.pi / 2
        L[:len(v)] += v * math.cos(th)
        R[:len(v)] += v * math.sin(th)
    st = np.stack([L, R], axis=1)
    nf = int(tail_fade * sr)
    st[-nf:] *= np.linspace(1, 0, nf)[:, None]
    st[:int(0.01 * sr)] *= np.linspace(0, 1, int(0.01 * sr))[:, None]
    return st

def save(name, st, sr, note):
    peak = np.abs(st).max()
    st = st / peak * (10 ** (-1 / 20))
    path = os.path.join(OUT, name)
    sf.write(path, st, sr, subtype="PCM_24")
    REPORT.append((name, len(st) / sr, 20 * math.log10(np.abs(st).max()), note))
    print(f"wrote {name}  {len(st)/sr:.1f}s")

def measure_lag(a, b, sr, t, win=3.0, maxlag=1.5):
    """量 b 相對 a 在時間 t 附近的延遲（秒），正值 = b 落後。"""
    n0 = int(t * sr); n1 = n0 + int(win * sr)
    A = a[n0:n1]; B = b[n0 - int(maxlag * sr):n1 + int(maxlag * sr)]
    A = (A - A.mean()); B = (B - B.mean())
    c = np.correlate(B, A, mode="valid")
    k = np.argmax(c)
    return (k - int(maxlag * sr)) / sr

# ---------------------------------------------------------------- 小星星素材
xx, SR1 = load_mono("中藥行小星星.wav")
A = cut(xx, SR1, 0.52, 19.90)            # 第一句：一閃一閃亮晶晶、滿天都是小星星
B1 = cut(xx, SR1, 19.90, 28.79)          # 第二句
B2 = cut(xx, SR1, 28.79, 37.95)          # 第三句
INTRO = cut(xx, SR1, 0.52, 37.95)        # 完整主題（A + B + B）
LA = len(A) / SR1
print(f"A phrase {LA:.2f}s, intro {len(INTRO)/SR1:.2f}s")

CTRL_HZ = 200
def timeline(dur, sr):
    n_out = int(dur * sr)
    n_ctrl = int(dur * CTRL_HZ) + 2
    t_ctrl = np.arange(n_ctrl) / CTRL_HZ
    return n_out, n_ctrl, t_ctrl

def grow_env(t_ctrl, t_start, t_full):
    return np.clip((t_ctrl - t_start) / (t_full - t_start), 0, 1)

def grid_reset_index(t_min, grid, sr):
    """回到理想脈衝（rate=1 時間軸）上、t_min 之後的第一個樂句邊界。"""
    k = math.ceil(t_min / grid)
    return int(round(k * grid * sr))

PANS5 = [-0.8, -0.4, 0.0, 0.4, 0.8]
GAINS5 = [1.0, 0.85, 0.9, 0.85, 0.8]

# 01 五聲部獨立漂移 ------------------------------------------------------
def render_01():
    dur = 100; sr = SR1
    n_out, n_ctrl, t_ctrl = timeline(dur, sr)
    rng = np.random.default_rng(1)
    env = grow_env(t_ctrl, 10, 45)
    voices = []; cents_all = []; poss = []
    for i in range(5):
        d = ou_drift(n_ctrl, 1 / CTRL_HZ, sigma_cents=6.0, theta=0.04, max_dev=14, rng=rng, env=env)
        cents_all.append(d)
        rate = cents_to_rate(to_audio_rate(d, t_ctrl, n_out, sr))
        v, p = render_voice(A, rate, sr=sr)
        voices.append(v * GAINS5[i]); poss.append(p)
    finish("01", voices, poss, sr, (20, 50, 80, 99), cents_all, t_ctrl, LA)
    save("01_小星星_五聲部獨立漂移.wav", pan_mix(voices, PANS5, sr), sr,
         "同一句 A 五聲部，前 10 秒完全同步，之後各自 random walk（上限 ±14 cents），不重新同步。")
    return cents_all

# 02 五聲部耦合漂移 -------------------------------------------------------
def render_02():
    dur = 100; sr = SR1
    n_out, n_ctrl, t_ctrl = timeline(dur, sr)
    rng = np.random.default_rng(1)
    env = grow_env(t_ctrl, 10, 45)
    D = coupled_drift(5, n_ctrl, 1 / CTRL_HZ, sigma_cents=6.0, theta=0.04, max_dev=14, coupling=0.8, rng=rng, env=env)
    voices = []; poss = []
    for i in range(5):
        rate = cents_to_rate(to_audio_rate(D[i], t_ctrl, n_out, sr))
        v, p = render_voice(A, rate, sr=sr)
        voices.append(v * GAINS5[i]); poss.append(p)
    finish("02", voices, poss, sr, (20, 50, 80, 99), list(D), t_ctrl, LA)
    save("02_小星星_五聲部耦合漂移.wav", pan_mix(voices, PANS5, sr), sr,
         "與 01 相同亂數種子，但加入 COUPLING=0.8：各聲部被拉向平均值，一起走音、彼此拉開得慢。")

# 03 漂移後重新同步 --------------------------------------------------------
def render_03():
    dur = 100; sr = SR1
    n_out, n_ctrl, t_ctrl = timeline(dur, sr)
    rng = np.random.default_rng(3)
    env = grow_env(t_ctrl, 8, 40)
    t_sync, tau = 58.0, 2.5
    grid = LA / 2                                   # 以半句（一行歌詞）為量化單位
    n_r = grid_reset_index(t_sync + 3.5 * tau, grid, sr)
    voices = []; poss = []; cents_all = []
    for i in range(5):
        d = ou_drift(n_ctrl, 1 / CTRL_HZ, sigma_cents=7.0, theta=0.03, max_dev=18, rng=rng, env=env)
        d = return_to_zero(d, t_ctrl, t_sync, tau)
        cents_all.append(d)
        rate = cents_to_rate(to_audio_rate(d, t_ctrl, n_out, sr))
        v, p = render_voice(A, rate, resets=[n_r], sr=sr)
        voices.append(v * GAINS5[i]); poss.append(p)
    finish("03", voices, poss, sr, (50, 57, 66, n_r / sr - 0.1, n_r / sr + 1, 90), cents_all, t_ctrl, LA / 2)
    save("03_小星星_漂移後重新同步.wav", pan_mix(voices, PANS5, sr), sr,
         f"漂移到 {t_sync:.0f} 秒觸發 SYNC：速率以 τ={tau}s 滑回原速，並在 {n_r/sr:.1f} 秒（下一個半句邊界）把五個聲部硬拉回句首。")

# 04 只動音準不動時間 -----------------------------------------------------
def render_04():
    sr = SR1
    cents = [0, 5, -7, 11, -3]
    passes = 3
    voices = []
    for i, c in enumerate(cents):
        v = librosa.effects.pitch_shift(A, sr=sr, n_steps=c / 100, bins_per_octave=12) if c else A.copy()
        v = np.tile(v, passes)
        voices.append(v * GAINS5[i])
    save("04_小星星_只動音準不動時間.wav", pan_mix(voices, PANS5, sr), sr,
         "對照組：五聲部固定 detune（0／+5／−7／+11／−3 cents）但時間完全對齊。這是 Pitch Hack 或 Pitch & Vibrato 的效果。")

# 05 glitch 事件 ------------------------------------------------------------
def render_05():
    dur = 100; sr = SR1
    n_out, n_ctrl, t_ctrl = timeline(dur, sr)
    rng = np.random.default_rng(5)
    env = grow_env(t_ctrl, 5, 35)
    t_sync, tau = 68.0, 2.0
    grid = LA / 2
    n_r = grid_reset_index(t_sync + 3.5 * tau, grid, sr)
    voices = []; poss = []; cents_all = []
    notes = []
    for i in range(5):
        d = ou_drift(n_ctrl, 1 / CTRL_HZ, sigma_cents=7.0, theta=0.03, max_dev=16, rng=rng, env=env)
        d = return_to_zero(d, t_ctrl, t_sync, tau)
        rate = cents_to_rate(to_audio_rate(d, t_ctrl, n_out, sr))
        amp = np.ones(n_out)
        resets = [n_r]
        overrides = []
        if i == 2:   # tape stop 於 35 s：1.2 s 減速到 0，靜止 0.4 s，然後從句首重來
            n0 = int(35 * sr); n1 = n0 + int(1.2 * sr); n2 = n1 + int(0.4 * sr)
            u = np.linspace(0, 1, n1 - n0)
            rate[n0:n1] *= (1 - u) ** 2
            rate[n1:n2] = 0
            amp[n0:n1] *= np.sqrt(1 - u)
            amp[n1:n2] = 0
            resets = [n2, n_r]
            notes.append("35.0s 聲部3 tape stop 後從句首重來")
        if i == 0:   # stutter 於 48 s：180 ms 片段重複 8 次
            n0 = int(48 * sr); g = int(0.18 * sr)
            p = np.cumsum(rate)[n0]
            idx = np.arange(8 * g)
            overrides.append((n0, n0 + 8 * g, p + (idx % g)))
            win = np.ones(g); f = int(0.005 * sr)
            win[:f] = np.linspace(0, 1, f); win[-f:] = np.linspace(1, 0, f)
            amp[n0:n0 + 8 * g] *= np.tile(win, 8)
            notes.append("48.0s 聲部1 buffer freeze 重複 8 次")
        if i == 3:   # reverse 於 55 s，2.4 s
            n0 = int(55 * sr); n1 = n0 + int(2.4 * sr)
            rate[n0:n1] *= -1
            notes.append("55.0s 聲部4 反轉 2.4 s")
        if i == 1:   # pitch fracture 於 62 s：八度上 0.6 s、八度下 0.6 s
            n0 = int(62 * sr); n1 = n0 + int(0.6 * sr); n2 = n1 + int(0.6 * sr)
            rate[n0:n1] *= 2.0
            rate[n1:n2] *= 0.5
            notes.append("62.0s 聲部2 八度斷裂")
        v, p = render_voice(A, rate, resets=resets, sr=sr, pos_override=overrides, amp=amp)
        voices.append(v * GAINS5[i]); poss.append(p); cents_all.append(d)
    finish("05", voices, poss, sr, (30, 60, n_r / sr - 0.1, n_r / sr + 1, 92), cents_all, t_ctrl, LA / 2)
    save("05_小星星_漂移與glitch事件.wav", pan_mix(voices, PANS5, sr), sr,
         "漂移中插入四個一次性事件（" + "；".join(notes) + f"），{t_sync:.0f} 秒觸發 SYNC，{n_r/sr:.1f} 秒硬對齊。")

# 06 wow / flutter 單聲部 ------------------------------------------------
def render_06():
    sr = SR1; dur = len(INTRO) / sr * 1.0
    n_out, n_ctrl, t_ctrl = timeline(dur, sr)
    rng = np.random.default_rng(6)
    wow = ou_drift(n_ctrl, 1 / CTRL_HZ, sigma_cents=40, theta=1.2, max_dev=25, rng=rng)   # 慢速不規則
    t = np.arange(n_out) / sr
    flutter = 3.0 * np.sin(2 * math.pi * 8.5 * t) * (0.6 + 0.4 * np.sin(2 * math.pi * 0.7 * t))
    cents = to_audio_rate(wow, t_ctrl, n_out, sr) + flutter
    rate = cents_to_rate(cents)
    v, _ = render_voice(INTRO, rate, sr=sr)
    save("06_小星星_完整主題_wow_flutter.wav", pan_mix([v], [0.0], sr, tail_fade=0.5), sr,
         "完整主題（三句）單聲部，只加 wow（±25 cents 不規則慢速）與 flutter（8.5 Hz ±3 cents）。這是 Magnetic 或 Echo Wobble 那一層的參考。")

# 07 四聲部漂移 + 半速低八度聲部 ----------------------------------------
def render_07():
    dur = 100; sr = SR1
    n_out, n_ctrl, t_ctrl = timeline(dur, sr)
    rng = np.random.default_rng(7)
    env = grow_env(t_ctrl, 10, 45)
    voices = []; poss = []; cents_all = []
    for i in range(4):
        d = ou_drift(n_ctrl, 1 / CTRL_HZ, sigma_cents=6.0, theta=0.04, max_dev=14, rng=rng, env=env)
        cents_all.append(d)
        rate = cents_to_rate(to_audio_rate(d, t_ctrl, n_out, sr))
        v, p = render_voice(A, rate, sr=sr)
        voices.append(v * GAINS5[i]); poss.append(p)
    d = ou_drift(n_ctrl, 1 / CTRL_HZ, sigma_cents=4.0, theta=0.04, max_dev=10, rng=rng, env=env)
    rate = 0.5 * cents_to_rate(to_audio_rate(d, t_ctrl, n_out, sr))
    v, p = render_voice(A, rate, sr=sr)
    voices.append(v * 0.9)
    finish("07", voices[:4], poss, sr, (20, 50, 80, 99), cents_all, t_ctrl, LA)
    save("07_小星星_四聲部漂移加半速低八度.wav", pan_mix(voices, [-0.7, -0.25, 0.25, 0.7, 0.0], sr), sr,
         "四聲部漂移同 01，多一個 rate=0.5 的聲部：低八度、兩倍長，像 cantus firmus 墊在下面。")

# ---------------------------------------------------------------- ㄅㄆㄇ 素材
bh, SR2 = load_mono("柏豪ㄅㄆㄇ.wav")
ay, _ = load_mono("阿瑤ㄅㄆㄇ.wav")
xs, _ = load_mono("小軒ㄅㄆㄇ.wav")
BPMF = cut(bh, SR2, 0.10, 2.45)          # 「ㄅㄆㄇㄈ」四個音節
BH_ALL = cut(bh, SR2, 0.05, 30.60)
AY_ALL = cut(ay, SR2, 0.35, 28.50)
XS_ALL = cut(xs, SR2, 0.30, 27.05)
LB = len(BPMF) / SR2

# 08 ㄅㄆㄇㄈ 四聲部 phase（固定偏移） -----------------------------------
def render_08():
    dur = 90; sr = SR2
    n_out = int(dur * sr)
    offsets = [0, 6, -6, 12]
    t_sync, tau = 62.0, 2.0
    n_r = grid_reset_index(t_sync + 3.5 * tau, LB, sr)
    t = np.arange(n_out) / sr
    voices = []; poss = []; cents_all = []
    for i, c in enumerate(offsets):
        cents = np.full(n_out, float(c))
        cents[t < 6] = 0                                              # 前 6 秒齊奏
        m = t >= t_sync
        cents[m] = c * np.exp(-(t[m] - t_sync) / tau)
        rate = cents_to_rate(cents)
        v, p = render_voice(BPMF, rate, resets=[n_r], sr=sr)
        voices.append(v); poss.append(p); cents_all.append(cents[::sr // CTRL_HZ])
    finish("08", voices, poss, sr, (10, 30, 55, n_r / sr - 0.1, n_r / sr + 1, 85), cents_all, t[::sr // CTRL_HZ], LB)
    save("08_ㄅㄆㄇㄈ_柏豪_四聲部phase.wav", pan_mix(voices, [-0.75, -0.25, 0.25, 0.75], sr), sr,
         f"柏豪的「ㄅㄆㄇㄈ」2.35 秒短句 ×4，固定偏移 0／+6／−6／+12 cents（Steve Reich 式 phasing），{t_sync:.0f} 秒 SYNC，{n_r/sr:.1f} 秒對齊。")

# 09 柏豪全段三聲部 random walk ------------------------------------------
def render_09():
    dur = 130; sr = SR2
    n_out, n_ctrl, t_ctrl = timeline(dur, sr)
    rng = np.random.default_rng(9)
    env = grow_env(t_ctrl, 5, 40)
    t_sync, tau = 88.0, 3.0
    Lall = len(BH_ALL) / sr
    n_r = grid_reset_index(t_sync + 3 * tau, Lall, sr)
    voices = []; poss = []; cents_all = []
    for i in range(3):
        d = ou_drift(n_ctrl, 1 / CTRL_HZ, sigma_cents=8.0, theta=0.03, max_dev=20, rng=rng, env=env)
        d = return_to_zero(d, t_ctrl, t_sync, tau)
        cents_all.append(d)
        rate = cents_to_rate(to_audio_rate(d, t_ctrl, n_out, sr))
        v, p = render_voice(BH_ALL, rate, resets=[n_r], sr=sr)
        voices.append(v); poss.append(p)
    finish("09", voices, poss, sr, (20, 60, 85, n_r / sr - 0.1, n_r / sr + 1), cents_all, t_ctrl, Lall)
    save("09_ㄅㄆㄇ_柏豪全段_三聲部漂移重同步.wav", pan_mix(voices, [-0.6, 0.0, 0.6], sr), sr,
         f"柏豪整段 30.5 秒 ×3，random walk 漂移（上限 ±20 cents），{t_sync:.0f} 秒 SYNC，{n_r/sr:.1f} 秒對齊到句首。")

# 10 三人：強制共同長度 → 釋放 → 重同步 ----------------------------------
def render_10():
    sr = SR2
    Lb = len(BH_ALL) / sr
    forced = [1.0, len(AY_ALL) / len(BH_ALL), len(XS_ALL) / len(BH_ALL)]   # 讓三人一句一樣長
    t_release, t_sync, tau = 2 * Lb, 150.0, 3.0
    n_r = grid_reset_index(t_sync + 3.5 * tau, Lb, sr)
    dur = n_r / sr + Lb + 1
    n_out = int(dur * sr)
    t = np.arange(n_out) / sr
    voices = []; poss = []; cents_all = []
    for src, fr in zip([BH_ALL, AY_ALL, XS_ALL], forced):
        rate = np.full(n_out, fr)
        m = (t >= t_release) & (t < t_release + 6)          # 6 秒內放回各自原速
        rate[m] = fr + (1 - fr) * (t[m] - t_release) / 6
        rate[t >= t_release + 6] = 1.0
        m2 = t >= t_sync                                    # SYNC：滑回強制速率
        rate[m2] = 1.0 + (fr - 1.0) * (1 - np.exp(-(t[m2] - t_sync) / tau))
        v, p = render_voice(src, rate, resets=[n_r], sr=sr)
        voices.append(v); poss.append(p); cents_all.append(1200 * np.log2(rate[::sr // CTRL_HZ]))
    finish("10", voices, poss, sr, (30, 70, 120, 149, n_r / sr + 1), cents_all, t[::sr // CTRL_HZ], Lb)
    save("10_ㄅㄆㄇ_三人_共同長度釋放重同步.wav", pan_mix(voices, [-0.6, 0.0, 0.6], sr), sr,
         f"柏豪原速；阿瑤、小軒先用 varispeed 拉到與柏豪同長（{1200*math.log2(forced[1]):+.0f}、{1200*math.log2(forced[2]):+.0f} cents），"
         f"兩輪後 {t_release:.0f} 秒釋放回原速讓三人自然散開，{t_sync:.0f} 秒 SYNC 拉回共同長度並在 {n_r/sr:.1f} 秒對齊句首。")

# ---------------------------------------------------------------- 執行
if __name__ == "__main__":
    which = sys.argv[1:] or ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10"]
    for w in which:
        globals()[f"render_{w}"]()
    with open(os.path.join(OUT, "README.md"), "w") as f:
        f.write("# 效果測試 2026-09-02\n\n")
        f.write("素材：`中藥行小星星.wav`（樂句邊界：第一句 0.52–19.90 s、第二句 19.90–28.79 s、第三句 28.79–37.95 s）、`柏豪ㄅㄆㄇ.wav`（「ㄅㄆㄇㄈ」0.10–2.45 s）、`阿瑤ㄅㄆㄇ.wav`、`小軒ㄅㄆㄇ.wav`。\n")
        f.write("除 04 之外全部是 varispeed：速度與音高綁定，等同 Classic Player 的 Transp 旋鈕被 LFO 推動。\n")
        f.write("所有聲部先 mono 再 pan，輸出 24-bit，峰值 −1 dBFS。\n\n")
        f.write("| 檔案 | 長度 | 內容 |\n|---|---|---|\n")
        for name, d, pk, note in REPORT:
            f.write(f"| `{name}` | {d:.0f} s | {note} |\n")
        f.write("\n## 聲部時間差量測（毫秒，聲部 1 為基準，正值＝落後）\n\n")
        for tag, tt, lags in LAGCHECK:
            f.write(f"- {tag} @ {tt} s：{lags}\n")
        f.write("\n## 不連續樣本檢查（相鄰 sample 跳動超過峰值 25% 的次數）\n\n")
        for tag, n in CLICKS: f.write(f"- {tag}：{n}\n")
        f.write("\n每個檔案附 `曲線_XX.png`：上圖各聲部 cents 偏移，下圖各聲部相對聲部 1 的時間差（毫秒），灰線為樂句邊界。\n")
        f.write("\n生成腳本：`render_effects.py`（同資料夾）。\n")
    import shutil; shutil.copy(__file__, os.path.join(OUT, "render_effects.py"))
    print(json.dumps(LAGCHECK, ensure_ascii=False)); print("clicks", CLICKS)
