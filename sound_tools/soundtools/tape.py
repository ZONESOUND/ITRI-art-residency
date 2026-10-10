"""磁帶與時間類效果：飽和、磁頭衰減、串音、tape echo、reverse delay、殘響。

全部是離線處理、純 numpy/scipy。單聲道 (n,) 或立體聲 (n,2) 皆可（逐聲道處理）。
來源：render_breath_tape.py（2026-09-07）、compose_v2.py（2026-09-03）、collage_lib.py（2026-09-15）。
"""
import math

import numpy as np
from scipy.signal import butter, fftconvolve, lfilter, sosfiltfilt

from .varispeed import cubic_read, wow_flutter


def _per_channel(fn, x, *a, **k):
    x = np.asarray(x, dtype=np.float64)
    if x.ndim == 1:
        return fn(x, *a, **k)
    return np.stack([fn(x[:, c], *a, **k) for c in range(x.shape[1])], axis=1)


def saturate(x, drive=1.4):
    """磁帶軟飽和。drive 越大越壓。"""
    return np.tanh(np.asarray(x) * drive) / math.tanh(drive)


def onepole_lp(x, sr, hz):
    b, a = butter(1, hz / (sr / 2))
    return _per_channel(lambda m: lfilter(b, a, m), x)


def lowpass(x, sr, hz, order=2):
    sos = butter(order, hz / (sr / 2), btype="low", output="sos")
    return _per_channel(lambda m: sosfiltfilt(sos, m), x)


def highpass(x, sr, hz, order=2):
    sos = butter(order, hz / (sr / 2), btype="high", output="sos")
    return _per_channel(lambda m: sosfiltfilt(sos, m), x)


def tape(x, sr, wow_cents=10.0, wow_theta=0.4, flutter_hz=7.0, flutter_cents=1.5,
         drive=1.4, head_hz=8000.0, seed=None):
    """一條磁帶鏈：varispeed wow/flutter → 飽和 → 磁頭高頻衰減。輸入輸出等長（循環讀取）。"""
    rng = np.random.default_rng(seed)
    x = np.asarray(x, dtype=np.float64)
    n = len(x)
    rate = wow_flutter(n, sr, wow_cents, wow_theta, flutter_hz, flutter_cents, rng)
    pos = np.cumsum(rate) - rate[0]
    y = _per_channel(lambda m: cubic_read(m, pos, loop=True), x)
    y = saturate(y, drive)
    return onepole_lp(y, sr, head_hz)


def crosstalk(tracks, sr, amount=0.045, delay_ms=1.2):
    """多軌機相鄰磁軌互相滲入。tracks 為等長單聲道清單。"""
    xt = int(delay_ms / 1000 * sr)
    orig = [t.copy() for t in tracks]
    out = [t.copy() for t in tracks]
    for k in range(len(out)):
        for j in (k - 1, k + 1):
            if 0 <= j < len(out):
                out[k][xt:] += orig[j][:-xt] * amount
    return out


def echo(x, sr, delay_s=0.35, fb=0.45, lp_hz=2800, taps=10, mix=1.0):
    """磁帶式回聲：每次回饋再過一次低通，非遞迴展開。輸出長度 = 原長 + taps × delay。"""
    x = np.asarray(x, dtype=np.float64)
    d = int(delay_s * sr)
    shape = (len(x) + taps * d,) + x.shape[1:]
    out = np.zeros(shape)
    out[:len(x)] += x
    cur = x.copy()
    for k in range(1, taps + 1):
        cur = onepole_lp(cur, sr, lp_hz) * fb
        out[k * d:k * d + len(cur)] += cur * mix
    return out


def reverse_delay(x, sr, delay_s=0.35, fb=0.55, lp_hz=3000, taps=8):
    """反轉 → 回聲 → 再反轉：回聲出現在本音之前（swell in）。回傳 (audio, 本音在輸出中的起點樣本)。"""
    e = echo(x[::-1], sr, delay_s, fb, lp_hz, taps)[::-1]
    return e, len(e) - len(x)


def reverse_delay_chunked(x, sr, delay_s=0.6, chunk_s=1.4, fb=0.45, mix=0.5):
    """切塊反轉再延遲送出（經典 reverse delay 踏板的做法）。輸出與輸入等長。"""
    x = np.asarray(x, dtype=np.float64)
    ch, dl = int(chunk_s * sr), int(delay_s * sr)
    out = np.zeros(len(x) + dl + ch)
    w = np.hanning(ch)
    g = mix
    for rep in range(4):
        if g < 0.01:
            break
        off = dl * (rep + 1)
        for n0 in range(0, len(x) - ch, ch // 2):
            p = n0 + off
            if p + ch < len(out):
                out[p:p + ch] += (x[n0:n0 + ch] * w)[::-1] * g
        g *= fb
    return out[:len(x)]


def noise_ir(sr, rt60=2.5, lp_hz=4000, predelay_ms=0.0, seed=0, stereo=True):
    """衰減雜訊脈衝響應。簡單、乾淨、不佔 CPU。"""
    r = np.random.default_rng(seed)
    n = int(rt60 * 1.3 * sr)
    t = np.arange(n) / sr
    ch = 2 if stereo else 1
    ir = r.standard_normal((n, ch)) * (10 ** (-3 * t / rt60))[:, None]
    ir = onepole_lp(ir, sr, lp_hz)
    ir[:int(0.005 * sr)] *= 0.2
    pre = np.zeros((int(predelay_ms / 1000 * sr), ch))
    ir = np.concatenate([pre, ir])
    ir /= np.sqrt((ir ** 2).sum(axis=0)).max()
    return ir if stereo else ir[:, 0]


def convolve(x, ir):
    """x 與 ir 逐聲道卷積；x 單聲道配立體聲 ir 會輸出立體聲。"""
    x = np.asarray(x, dtype=np.float64)
    if ir.ndim == 1:
        return _per_channel(lambda m: fftconvolve(m, ir), x)
    if x.ndim == 1:
        return np.stack([fftconvolve(x, ir[:, c]) for c in range(ir.shape[1])], axis=1)
    return np.stack([fftconvolve(x[:, c], ir[:, c]) for c in range(ir.shape[1])], axis=1)


def reverb(x, sr, rt60=2.5, lp_hz=4000, predelay_ms=20, mix=0.3, seed=1):
    """合成殘響，濕訊號與乾訊號等 RMS 後依 mix 混合。輸出含尾巴。"""
    x = np.asarray(x, dtype=np.float64)
    ir = noise_ir(sr, rt60, lp_hz, predelay_ms, seed, stereo=(x.ndim == 2))
    wet = convolve(x, ir)
    wet *= np.sqrt(np.mean(x ** 2)) / (np.sqrt(np.mean(wet ** 2)) + 1e-9)
    pad = np.zeros((len(wet) - len(x),) + x.shape[1:])
    return np.concatenate([x, pad]) * (1 - mix) + wet * mix


def _fdn_impulse(sr, rt60, size=1.0, damp=0.35):
    delays = [int(d * size) for d in (1931, 2467, 3121, 3739)]
    g = [10 ** (-3.0 * d / sr / rt60) for d in delays]
    n = int(rt60 * 1.5 * sr)
    bufs = [np.zeros(d) for d in delays]
    idx = [0] * 4
    z = [0.0] * 4
    H = 0.5 * np.array([[1, 1, 1, 1], [1, -1, 1, -1], [1, 1, -1, -1], [1, -1, -1, 1]], dtype=np.float64)
    out = np.zeros(n)
    for i in range(n):
        r = np.array([bufs[k][idx[k]] for k in range(4)])
        for k in range(4):
            z[k] = (1 - damp) * r[k] + damp * z[k]
            r[k] = z[k]
        s = H @ r
        inp = 1.0 if i == 0 else 0.0
        for k in range(4):
            bufs[k][idx[k]] = inp + s[k] * g[k]
            idx[k] = (idx[k] + 1) % delays[k]
        out[i] = r.sum() * 0.25
    return out


def fdn_reverb(x, sr, rt60=3.0, mix=0.3, size=1.0):
    """4 線 FDN 殘響：先算脈衝響應再 FFT 卷積（逐樣本迴圈只跑 IR 長度）。輸出與輸入等長。"""
    x = np.asarray(x, dtype=np.float64)
    ir = _fdn_impulse(sr, rt60, size)
    wet = _per_channel(lambda m: fftconvolve(m, ir)[:len(m)], x)
    wet *= np.max(np.abs(x)) / (np.max(np.abs(wet)) + 1e-12)
    return x * (1 - mix) + wet * mix


def hiss(n, sr, level_db=-58.0, lp_hz=4000, seed=0):
    r = np.random.default_rng(seed)
    h = onepole_lp(r.standard_normal((n, 2)), sr, lp_hz)
    return h * 10 ** (level_db / 20)


def tape_stop(x, sr, t_stop, dur=1.2, hold=0.4):
    """在 t_stop 秒開始減速到停（音高下滑、音量收掉），hold 秒靜音。輸入輸出等長。"""
    x = np.asarray(x, dtype=np.float64)
    n = len(x)
    rate = np.ones(n); amp = np.ones(n)
    n0 = int(t_stop * sr); n1 = min(n0 + int(dur * sr), n); n2 = min(n1 + int(hold * sr), n)
    u = np.linspace(0, 1, n1 - n0)
    rate[n0:n1] = (1 - u) ** 2; rate[n1:n2] = 0
    amp[n0:n1] = np.sqrt(1 - u); amp[n1:n2] = 0
    pos = np.cumsum(rate) - rate[0]
    y = _per_channel(lambda m: cubic_read(m, pos, loop=False), x)
    return y * (amp if x.ndim == 1 else amp[:, None])
