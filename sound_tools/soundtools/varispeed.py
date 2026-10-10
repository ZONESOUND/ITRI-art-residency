"""變速讀取與漂移：速度與音高綁定（tape varispeed），多聲部漂移、耦合、回歸、量化硬對齊。

單位：偏移量一律 cents；rate 1.0 = 原速。控制率曲線先用 CTRL_HZ 算，再內插到音訊率。
來源：《節奏繞纏》效果測試 render_effects.py（2026-09-02）與 render_breath_tape.py（2026-09-07）。
"""
import math

import numpy as np

CTRL_HZ = 200


def cents_to_rate(c):
    return 2.0 ** (np.asarray(c, dtype=np.float64) / 1200.0)


def cubic_read(src, pos, loop=True):
    """4 點 Catmull-Rom 內插讀取。pos 以樣本為單位。loop=True 自動 wrap，否則越界回 0。"""
    L = len(src)
    if loop:
        pos = np.mod(pos, L)
        i1 = np.floor(pos).astype(np.int64)
        f = pos - i1
        i0, i2, i3 = (i1 - 1) % L, (i1 + 1) % L, (i1 + 2) % L
        valid = 1.0
    else:
        valid = ((pos >= 1) & (pos < L - 2)).astype(np.float64)
        p = np.clip(pos, 1, L - 3)
        i1 = np.floor(p).astype(np.int64)
        f = p - i1
        i0, i2, i3 = i1 - 1, i1 + 1, i1 + 2
    p0, p1, p2, p3 = src[i0], src[i1], src[i2], src[i3]
    out = p1 + 0.5 * f * (p2 - p0 + f * (2 * p0 - 5 * p1 + 4 * p2 - p3 + f * (3 * (p1 - p2) + p3 - p0)))
    return out * valid


def varispeed(src, cents, sr=None, loop=False):
    """固定或逐樣本 cents 的變速播放（非循環）。cents 可為常數或陣列。"""
    src = np.asarray(src, dtype=np.float64)
    if np.isscalar(cents):
        rate = float(cents_to_rate(cents))
        pos = np.arange(int(len(src) / rate)) * rate
    else:
        rate = cents_to_rate(cents)
        pos = np.cumsum(rate) - rate[0]
        pos = pos[: int(np.searchsorted(pos, len(src)))]
    return cubic_read(src, pos, loop=loop)


# ------------------------------------------------------------------ 漂移曲線（控制率）

def ou_drift(n_ctrl, dt, sigma, theta, max_dev, rng, env=None):
    """Ornstein-Uhlenbeck random walk（cents）：sigma 步伐、theta 均值回歸、max_dev 上限、env 隨時間放大。"""
    d = np.zeros(n_ctrl)
    x = 0.0
    for k in range(1, n_ctrl):
        e = 1.0 if env is None else env[k]
        x += -theta * x * dt + sigma * e * math.sqrt(dt) * rng.standard_normal()
        x = max(-max_dev, min(max_dev, x))
        d[k] = x
    return d


def coupled_drift(K, n_ctrl, dt, sigma, theta, max_dev, coupling, rng, env=None):
    """K 個聲部的 OU 漂移，加上把各聲部拉向平均值的耦合項。coupling 0 = 各自獨立。"""
    d = np.zeros((K, n_ctrl))
    x = np.zeros(K)
    for k in range(1, n_ctrl):
        e = 1.0 if env is None else env[k]
        x += (-theta * x + coupling * (x.mean() - x)) * dt + sigma * e * math.sqrt(dt) * rng.standard_normal(K)
        x = np.clip(x, -max_dev, max_dev)
        d[:, k] = x
    return d


def return_to_zero(d_ctrl, t_ctrl, t_sync, tau):
    """從 t_sync 起偏移量以時間常數 tau 指數衰減回 0（return speed）。"""
    d = d_ctrl.copy()
    k0 = int(np.searchsorted(t_ctrl, t_sync))
    if k0 < len(d):
        d[k0:] = d[k0] * np.exp(-(t_ctrl[k0:] - t_sync) / tau)
    return d


def wow_flutter(n, sr, wow_cents=10.0, wow_theta=0.4, flutter_hz=7.0, flutter_cents=1.5, rng=None):
    """磁帶速率曲線：慢速不規則 wow（OU）加固定頻率 flutter。回傳每樣本 rate。"""
    rng = rng or np.random.default_rng()
    ctrl = 100.0
    n_ctrl = int(n / sr * ctrl) + 2
    t_ctrl = np.arange(n_ctrl) / ctrl
    wow = ou_drift(n_ctrl, 1 / ctrl, wow_cents, wow_theta, wow_cents * 2.5, rng)
    t = np.arange(n) / sr
    cents = np.interp(t, t_ctrl, wow) + flutter_cents * np.sin(2 * np.pi * flutter_hz * t + rng.uniform(0, 2 * np.pi))
    return cents_to_rate(cents)


def timeline(dur, sr, ctrl_hz=CTRL_HZ):
    n_out = int(dur * sr)
    n_ctrl = int(dur * ctrl_hz) + 2
    return n_out, n_ctrl, np.arange(n_ctrl) / ctrl_hz


def to_audio_rate(ctrl, t_ctrl, n_out, sr):
    return np.interp(np.arange(n_out) / sr, t_ctrl, ctrl)


def grow_env(t_ctrl, t_start, t_full):
    return np.clip((t_ctrl - t_start) / max(1e-9, t_full - t_start), 0, 1)


def grid_reset_index(t_min, grid, sr):
    """理想脈衝（rate = 1）時間軸上、t_min 之後的第一個樂句邊界（樣本索引）。"""
    return int(round(math.ceil(t_min / grid) * grid * sr))


# ------------------------------------------------------------------ 循環聲部 render

def render_loop_voice(src, rate, sr, resets=(), pos0=0.0, cf_ms=30, amp=None):
    """循環播放 src，rate 為每樣本速率。resets 的樣本點把讀取位置硬拉回 loop 起點（帶 crossfade）。
    回傳 (audio, pos)；pos 可用來精確計算聲部間的時間差。"""
    src = np.asarray(src, dtype=np.float64)
    pos = np.cumsum(rate) - rate[0] + pos0
    wins = []
    for n_r in resets:
        if n_r < len(pos):
            c = pos[n_r]
            pos[n_r:] -= c
            wins.append((n_r, c))
    out = cubic_read(src, pos, loop=True)
    cf = int(cf_ms * sr / 1000)
    for n_r, c in wins:
        n1 = min(n_r + cf, len(pos))
        old = cubic_read(src, pos[n_r:n1] + c, loop=True)
        w = np.linspace(0, 1, n1 - n_r)
        out[n_r:n1] = old * (1 - w) + out[n_r:n1] * w
    if amp is not None:
        out = out * amp
    return out, pos


def drift_ensemble(src, sr, dur, voices=5, sigma=7.0, theta=0.03, max_dev=16.0, coupling=0.0,
                   grow=(8.0, 40.0), t_sync=None, tau=2.5, grid=None, rate_base=None, seed=1):
    """一段 loop 做多聲部漂移。t_sync 給定時從該秒滑回原速，並在下一個 grid 邊界硬對齊句首。
    grid 預設為 loop 長度的一半。rate_base 可給每聲部基礎速率（例如 0.5 做低八度）。
    回傳 dict：voices（各聲部單軌）、pos、cents（控制率曲線）、t_ctrl、reset_sample。"""
    rng = np.random.default_rng(seed)
    n_out, n_ctrl, t_ctrl = timeline(dur, sr)
    env = grow_env(t_ctrl, *grow)
    D = coupled_drift(voices, n_ctrl, 1 / CTRL_HZ, sigma, theta, max_dev, coupling, rng, env)
    if grid is None:
        grid = len(src) / sr / 2
    resets = []
    n_r = None
    if t_sync is not None:
        n_r = grid_reset_index(t_sync + 3.5 * tau, grid, sr)
        if n_r < n_out:
            resets = [n_r]
    outs, poss, cents = [], [], []
    for i in range(voices):
        d = D[i] if t_sync is None else return_to_zero(D[i], t_ctrl, t_sync, tau)
        rb = 1.0 if rate_base is None else rate_base[i]
        rate = rb * cents_to_rate(to_audio_rate(d, t_ctrl, n_out, sr))
        v, p = render_loop_voice(src, rate, sr, resets=resets)
        outs.append(v); poss.append(p); cents.append(d)
    return dict(voices=outs, pos=poss, cents=cents, t_ctrl=t_ctrl, reset_sample=n_r)


def lag_ms(poss, sr, t):
    """各聲部相對聲部 0 在 t 秒的時間差（毫秒），由讀取位置直接計算，不用互相關。"""
    n = min(int(t * sr), len(poss[0]) - 1)
    return [round(float(p[n] - poss[0][n]) / sr * 1000, 1) for p in poss[1:]]


def pan_mix(voices, pans, sr, tail_fade=2.0):
    """多個單聲道聲部依 pan（-1..1）等功率混成立體聲。"""
    n = max(len(v) for v in voices)
    L = np.zeros(n); R = np.zeros(n)
    for v, p in zip(voices, pans):
        th = (p + 1) / 2 * math.pi / 2
        L[:len(v)] += v * math.cos(th); R[:len(v)] += v * math.sin(th)
    st = np.stack([L, R], axis=1)
    nf = min(int(tail_fade * sr), n)
    if nf > 0:
        st[-nf:] *= np.linspace(1, 0, nf)[:, None]
    return st
