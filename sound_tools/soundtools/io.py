"""讀寫、取樣率、電平與淡入淡出。所有模組共用。

內部格式：float64。單聲道為 (n,)，立體聲為 (n, 2)。
"""
import math
import os
import subprocess

import numpy as np
import soundfile as sf
from scipy.signal import resample_poly


def load(path, sr=None, mono=False):
    """讀 wav／aif／flac；mp3 走 ffmpeg。回傳 (audio, sr)。sr 指定時重取樣。"""
    path = os.path.expanduser(path)
    if path.lower().endswith((".mp3", ".m4a")):
        target = sr or 48000
        raw = subprocess.run(
            ["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "2", "-ar", str(target), "-"],
            capture_output=True, check=True).stdout
        y = np.frombuffer(raw, dtype=np.float32).reshape(-1, 2).astype(np.float64)
        s = target
    else:
        y, s = sf.read(path, always_2d=True)
        y = y.astype(np.float64)
    if y.shape[1] > 2:
        y = y[:, :2]
    if sr and s != sr:
        g = math.gcd(sr, s)
        y = resample_poly(y, sr // g, s // g, axis=0)
        s = sr
    if mono:
        y = y.mean(axis=1)
    elif y.shape[1] == 1:
        y = y[:, 0]
    return y, s


def to_mono(x):
    return x.mean(axis=1) if x.ndim == 2 else x


def to_stereo(x):
    return np.stack([x, x], axis=1) if x.ndim == 1 else x


def peak_norm(x, peak_db=-1.0):
    p = np.max(np.abs(x))
    return x * (10 ** (peak_db / 20) / p) if p > 0 else x


def db(g):
    return 10 ** (g / 20)


def fade(x, sr, in_s=0.01, out_s=0.01, equal_power=True):
    x = np.array(x, dtype=np.float64, copy=True)
    n = len(x)
    fi, fo = min(int(in_s * sr), n), min(int(out_s * sr), n)
    if fi > 0:
        r = np.linspace(0, 1, fi)
        w = np.sin(r * math.pi / 2) if equal_power else r
        x[:fi] *= w if x.ndim == 1 else w[:, None]
    if fo > 0:
        r = np.linspace(1, 0, fo)
        w = np.sin(r * math.pi / 2) if equal_power else r
        x[n - fo:] *= w if x.ndim == 1 else w[:, None]
    return x


def lufs(x, sr):
    """整段響度（需要 pyloudnorm）。太短或靜音回 -70。"""
    import pyloudnorm as pyln
    x = to_stereo(x)
    if len(x) < sr * 0.4:
        return -70.0
    v = pyln.Meter(sr).integrated_loudness(x)
    return -70.0 if not np.isfinite(v) else float(v)


def norm_lufs(x, sr, target=-20.0):
    cur = lufs(x, sr)
    return x if cur <= -69 else x * 10 ** ((target - cur) / 20)


def write(path, x, sr, subtype="PCM_24", peak_db=None, mp3=False):
    """寫 wav。peak_db 給定時先正規化峰值；mp3=True 另存 192k mp3 試聽檔。"""
    path = os.path.expanduser(path)
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    x = np.asarray(x, dtype=np.float64)
    if peak_db is not None:
        x = peak_norm(x, peak_db)
    sf.write(path, np.clip(x, -1, 1), sr, subtype=subtype)
    if mp3:
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", path, "-codec:a", "libmp3lame", "-b:a", "192k",
                        os.path.splitext(path)[0] + ".mp3"], check=True)
    return path


def discontinuities(x, frac=0.25):
    """相鄰樣本跳動超過峰值 frac 倍的次數。爆破音與響亮母音也會算進去，只當警訊。"""
    m = to_mono(x)
    d = np.abs(np.diff(m))
    return int((d > frac * np.abs(m).max()).sum())
