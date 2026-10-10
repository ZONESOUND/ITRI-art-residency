"""拼貼與時間軸：交叉淡化串接、循環、疊放、慢速電平器、paulstretch、顆粒雲、最後鏈。

來源：collage_lib.py（2026-09-15）、render_backing_pads.py（2026-09-08）。
"""
import math

import numpy as np
from scipy.signal import lfilter

from .io import db, fade, lufs, norm_lufs, to_mono, to_stereo


def timeline(dur_s, sr, stereo=True):
    n = int(dur_s * sr)
    return np.zeros((n, 2)) if stereo else np.zeros(n)


def place(bus, seg, sr, t, gain_db=0.0, pan=0.0, fade_s=0.0):
    """把 seg 疊到 bus 的 t 秒處。bus 立體聲時 pan -1..1 等功率；bus 單聲道時忽略 pan。超出尾端自動截。"""
    seg = np.asarray(seg, dtype=np.float64)
    if fade_s > 0:
        seg = fade(seg, sr, fade_s, fade_s)
    n0 = int(t * sr)
    if n0 >= len(bus) or n0 + len(seg) <= 0:
        return
    if n0 < 0:
        seg = seg[-n0:]; n0 = 0
    seg = seg[:len(bus) - n0]
    g = db(gain_db)
    if bus.ndim == 1:
        bus[n0:n0 + len(seg)] += to_mono(seg) * g
        return
    seg = to_stereo(seg)
    th = (pan + 1) / 2 * math.pi / 2
    bus[n0:n0 + len(seg), 0] += seg[:, 0] * math.cos(th) * math.sqrt(2) * g
    bus[n0:n0 + len(seg), 1] += seg[:, 1] * math.sin(th) * math.sqrt(2) * g


def xfade_concat(segs, sr, xf_s=3.0):
    """等功率交叉淡化串接。xf_s 單一值或每個接縫一個的清單。"""
    segs = [np.asarray(s, dtype=np.float64) for s in segs]
    if isinstance(xf_s, (int, float)):
        xf_s = [xf_s] * (len(segs) - 1)
    out = segs[0].copy()
    for s, xf in zip(segs[1:], xf_s):
        n = int(min(xf * sr, len(out), len(s)))
        if n <= 0:
            out = np.concatenate([out, s]); continue
        r = np.linspace(0, 1, n)
        a, b = np.cos(r * math.pi / 2), np.sin(r * math.pi / 2)
        if out.ndim == 2:
            a, b = a[:, None], b[:, None]
        mid = out[-n:] * a + s[:n] * b
        out = np.concatenate([out[:-n], mid, s[n:]])
    return out


def loop_to(x, sr, dur_s, xf_s=2.0):
    """把素材循環到 dur_s 秒，接縫交叉淡化。"""
    x = np.asarray(x, dtype=np.float64)
    need = int(dur_s * sr)
    if len(x) >= need:
        return x[:need]
    pieces = [x] * (need // max(1, len(x) - int(xf_s * sr)) + 2)
    return xfade_concat(pieces, sr, xf_s)[:need]


def leveler(x, sr, win_s=2.0, max_gain_db=12.0, target_rms_db=None, floor_db=-60.0):
    """慢速電平器（很慢的 AGC）：用 win_s 秒 RMS 包絡把起伏拉平到 target，增益限 ±max_gain_db，真靜音不拉。"""
    x = np.asarray(x, dtype=np.float64)
    m = to_mono(x)
    n = len(m)
    hop = int(sr * 0.05); win = int(sr * win_s)
    cs = np.concatenate([[0], np.cumsum(m ** 2)])
    env = np.zeros(n // hop + 1)
    for k in range(len(env)):
        c = k * hop
        a, b = max(0, c - win // 2), min(n, c + win // 2)
        env[k] = math.sqrt((cs[b] - cs[a]) / max(1, b - a) + 1e-12)
    env_db = 20 * np.log10(env + 1e-9)
    if target_rms_db is None:
        target_rms_db = float(np.median(env_db[env_db > floor_db])) if np.any(env_db > floor_db) else -20
    gain_db = np.clip(target_rms_db - env_db, -max_gain_db, max_gain_db)
    gain_db[env_db < floor_db] = 0.0
    alpha = math.exp(-1 / (win_s / 0.05 * 0.5))
    g = np.zeros_like(gain_db); acc = gain_db[0]
    for k in range(len(gain_db)):
        acc = alpha * acc + (1 - alpha) * gain_db[k]; g[k] = acc
    gain = np.interp(np.arange(n), np.arange(len(g)) * hop, db(g))
    return x * (gain if x.ndim == 1 else gain[:, None])


def compress(x, sr, thresh_db=-18, ratio=3.0, attack_s=0.03, release_s=0.4):
    x = np.asarray(x, dtype=np.float64)
    m = np.abs(to_mono(x))
    aa, ar = math.exp(-1 / (attack_s * sr)), math.exp(-1 / (release_s * sr))
    env = np.maximum(lfilter([1 - ar], [1, -ar], m), lfilter([1 - aa], [1, -aa], m))
    over = np.maximum(0, 20 * np.log10(env + 1e-9) - thresh_db)
    g = db(-over * (1 - 1 / ratio))
    return x * (g if x.ndim == 1 else g[:, None])


def limiter(x, sr, ceiling_db=-3.0, lookahead_s=0.005, release_s=0.1):
    x = np.asarray(x, dtype=np.float64)
    c = db(ceiling_db)
    peak = np.abs(x) if x.ndim == 1 else np.max(np.abs(x), axis=1)
    la = int(lookahead_s * sr)
    pk = np.maximum.reduce([np.pad(peak, (0, k))[k:] for k in range(0, la, max(1, la // 8))] + [peak])
    need = np.minimum(1.0, c / (pk + 1e-9))
    ar = math.exp(-1 / (release_s * sr))
    g = np.ones(len(need)); acc = 1.0
    for k in range(len(need)):
        acc = need[k] if need[k] < acc else ar * acc + (1 - ar) * need[k]
        g[k] = acc
    return x * (g if x.ndim == 1 else g[:, None])


def finalize(x, sr, target_lufs=-20.0, tp_db=-3.0, level_win_s=3.0, level_max_db=16.0,
             fine_win_s=1.0, fine_max_db=6.0, comp=True, edge_fade_s=1.0):
    """最後鏈：粗電平器 → 細電平器 → 軟壓縮 → 響度正規化 → 限幅 → 再校正 → 頭尾短淡化。需要 pyloudnorm。"""
    y = leveler(x, sr, level_win_s, level_max_db)
    y = leveler(y, sr, fine_win_s, fine_max_db)
    if comp:
        y = compress(y, sr)
    y = limiter(norm_lufs(y, sr, target_lufs), sr, tp_db)
    y = limiter(norm_lufs(y, sr, target_lufs), sr, tp_db)
    return fade(y, sr, edge_fade_s, edge_fade_s)


def paulstretch(x, stretch=8.0, win=16384, seed=0):
    """Paul Nasca 的 paulstretch（相位隨機化極慢拉伸）。x 單聲道或立體聲。視窗只讀真實輸入，尾端不補零。"""
    rng = np.random.default_rng(seed)
    x = to_stereo(np.asarray(x, dtype=np.float64)); n, ch = x.shape
    half = win // 2
    w = (1 - np.linspace(-1, 1, win) ** 2) ** 1.25
    displace = half / stretch
    out_len = int(n * stretch) + win
    out = np.zeros((out_len, ch)); norm = np.zeros(out_len)
    pos = 0.0; o = 0
    while o + win < out_len and pos + win <= n:
        i = int(pos)
        spec = np.fft.rfft(x[i:i + win] * w[:, None], axis=0)
        ph = np.exp(1j * rng.uniform(0, 2 * np.pi, size=spec.shape))
        y = np.fft.irfft(np.abs(spec) * ph, n=win, axis=0) * w[:, None]
        out[o:o + win] += y; norm[o:o + win] += w ** 2
        o += half; pos += displace
    norm[norm < 1e-6] = 1
    return out[:o] / norm[:o, None]


def granular(material, sr, length_s, grain_ms=(150, 300), density=40, pitch_jitter_cents=15, rate=1.0, seed=1):
    """顆粒雲：隨機取位置、Hann 窗、每粒微 detune，rate 控整體速度（0.5 = 低八度）。大粒子加高密度 = 平滑的雲。"""
    r = np.random.default_rng(seed)
    material = to_stereo(np.asarray(material, dtype=np.float64))
    n = int(length_s * sr); out = np.zeros((n + sr, 2))
    idx = np.arange(len(material))
    for s in np.sort(r.uniform(0, length_s, int(length_s * density))):
        g_out = int(r.uniform(*grain_ms) / 1000 * sr)
        ratio = rate * 2 ** (r.normal(0, pitch_jitter_cents) / 1200)
        g_in = int(g_out * ratio)
        if g_in >= len(material) - 1:
            continue
        p = int(r.uniform(0, len(material) - g_in - 1))
        src = np.linspace(p, p + g_in, g_out, endpoint=False)
        g = np.stack([np.interp(src, idx, material[:, c]) for c in range(2)], axis=1) * np.hanning(g_out)[:, None]
        pan = r.uniform(0.3, 0.7); g *= np.array([np.sqrt(1 - pan), np.sqrt(pan)])
        o = int(s * sr); out[o:o + g_out] += g
    return out[:n]
