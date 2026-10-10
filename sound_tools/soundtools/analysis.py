"""分析：樂句邊界（旋律型態比對）、語音音節切分（停頓、能量峰、音素辨識三路交叉）、stems 回對原檔。

方法與坑的說明在 Obsidian `Tools/MIR 音訊分析方法.md`。
來源：效果測試_20260902 的即時分析程式（2026-09-02/03，首次整理成檔）、analyze_stems.py（2026-09-06）。
"""
import math
import os
import subprocess
import tempfile

import numpy as np
import soundfile as sf
from scipy.ndimage import median_filter, uniform_filter1d
from scipy.signal import fftconvolve, find_peaks, resample_poly

from .io import to_mono

NOTE = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


# ------------------------------------------------------------------ 樂句邊界

def notes(x, sr, fmin=100, fmax=1200, hop=256, min_len=0.08, merge_gap=0.12):
    """pyin 音高追蹤 → 半音取整 → 中值濾波 → 合併成音符。回傳 [(start, end, midi), ...]。"""
    import librosa
    m = to_mono(x)
    f0, vf, _ = librosa.pyin(m, fmin=fmin, fmax=fmax, sr=sr, frame_length=2048, hop_length=hop)
    t = librosa.frames_to_time(np.arange(len(f0)), sr=sr, hop_length=hop)
    midi = np.where(vf, librosa.hz_to_midi(f0), np.nan)
    mr = np.round(median_filter(np.nan_to_num(midi, nan=-1), size=9))
    out, cur = [], None
    for i, v in enumerate(mr):
        if v < 0:
            if cur: out.append(cur); cur = None
            continue
        if cur and cur[2] == v:
            cur[1] = t[i]
        else:
            if cur: out.append(cur)
            cur = [t[i], t[i], int(v)]
    if cur: out.append(cur)
    out = [n for n in out if n[1] - n[0] >= min_len]
    merged = []
    for n in out:
        if merged and merged[-1][2] == n[2] and n[0] - merged[-1][1] < merge_gap:
            merged[-1][1] = n[1]
        else:
            merged.append(list(n))
    return [tuple(n) for n in merged]


def find_motif(note_list, intervals):
    """在音符序列中找相對音程型態。intervals 例：小星星開頭 [0, 7, 9, 7]（重複音已被合併）。回傳 [(start_s, root_midi)]。"""
    seq = [n[2] for n in note_list]
    hits = []
    k = len(intervals)
    for i in range(len(seq) - k + 1):
        a = seq[i]
        if [s - a for s in seq[i:i + k]] == list(intervals):
            hits.append((note_list[i][0], a))
    return hits


def phrases_by_motif(x, sr, patterns=((0, 7, 9, 7), (0, -2, -3, -5)), lead_s=0.05, min_gap=8.0, **kw):
    """用一個以上的旋律型態找樂句起點（預設兩個是小星星的 A 句頭與 B 句頭），切點取句首音起音前 lead_s 秒。
    距離前一個句首不到 min_gap 秒的命中視為句內的半句，不切。回傳 ([(start, end)], notes, hits)，最後一句到檔尾。"""
    nl = notes(x, sr, **kw)
    hits = sorted(set(h for pat in patterns for h in find_motif(nl, pat)))
    starts = []
    for t, _ in hits:
        if not starts or t - starts[-1] >= min_gap:
            starts.append(max(0.0, t - lead_s))
    ends = starts[1:] + [len(to_mono(x)) / sr]
    return list(zip(starts, ends)), nl, hits


# ------------------------------------------------------------------ 音節切分

def pauses(x, sr, top_db=30, gap=0.3, min_len=0.12):
    """停頓切段：回傳發聲區段 [(start, end)]。"""
    import librosa
    m = to_mono(x)
    iv = librosa.effects.split(m, top_db=top_db, frame_length=2048, hop_length=512) / sr
    out = []
    for s, e in iv:
        if out and s - out[-1][1] < gap:
            out[-1][1] = e
        else:
            out.append([s, e])
    return [(s, e) for s, e in out if e - s >= min_len]


def syllable_peaks(x, sr, prominence=5.0, min_dist=0.3, height_db=-38.0, edge_db=18.0, hop=128):
    """音節能量峰：RMS dB 平滑後 find_peaks。回傳 [(start, end, peak_t)]，邊界為峰值兩側下降 edge_db 或局部最低。"""
    import librosa
    m = to_mono(x)
    rms = librosa.feature.rms(y=m, frame_length=512, hop_length=hop)[0]
    dbs = uniform_filter1d(20 * np.log10(rms + 1e-6), 9)
    t = np.arange(len(dbs)) * hop / sr
    pk, _ = find_peaks(dbs, prominence=prominence, distance=int(min_dist * sr / hop), height=height_db)
    out = []
    for i in pk:
        thr = dbs[i] - edge_db
        a = i
        while a > 0 and dbs[a - 1] < dbs[a] and dbs[a - 1] > thr:
            a -= 1
        while a > 0 and dbs[a - 1] <= dbs[a]:
            a -= 1
        b = i
        while b < len(dbs) - 1 and dbs[b + 1] < dbs[b] and dbs[b + 1] > thr:
            b += 1
        while b < len(dbs) - 1 and dbs[b + 1] <= dbs[b]:
            b += 1
        out.append((float(t[a]), float(t[b]), float(t[i])))
    merged = []
    for h in out:
        if merged and h[0] < merged[-1][1] - 0.05:
            merged[-1] = (merged[-1][0], max(merged[-1][1], h[1]), merged[-1][2])
        else:
            merged.append(h)
    return merged


def phones(x, sr, lang="cmn", emit=1.0):
    """allosaurus 音素辨識（需另外安裝）。回傳 [(t, phone)]。母音與鼻韻可靠，子音段可靠度低。"""
    m = to_mono(x)
    y = resample_poly(m, 16000 // math.gcd(16000, sr), sr // math.gcd(16000, sr)) if sr != 16000 else m
    try:
        import allosaurus  # noqa: F401
    except ImportError:
        import sys
        print("allosaurus 未安裝：uv sync --extra phones", file=sys.stderr)
        return []
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "a.wav")
        sf.write(p, y, 16000, subtype="PCM_16")
        r = subprocess.run(["python", "-m", "allosaurus.run", "--lang", lang, "--timestamp", "True",
                            "-e", str(emit), "-i", p], capture_output=True, text=True)
    out = []
    for line in r.stdout.splitlines():
        parts = line.split()
        if len(parts) >= 3:
            try:
                out.append((float(parts[0]), parts[2]))
            except ValueError:
                pass
    return out


def syllables(x, sr, expected=None, with_phones=False):
    """三路交叉的音節報告：停頓段、能量峰（含每段峰數）、可選的音素。expected 給定時標出峰數不合的段。
    不做強制對齊；計數不合要人工決定多出來的是哪一個。"""
    seg = pauses(x, sr)
    pk = syllable_peaks(x, sr)
    ph = phones(x, sr) if with_phones else []
    report = []
    for i, (s, e) in enumerate(seg):
        peaks = [p for p in pk if s - 0.05 <= p[2] <= e + 0.05]
        inside = [q for (t, q) in ph if s - 0.08 <= t <= e]
        row = dict(idx=i, start=round(s, 2), end=round(e, 2), n_peaks=len(peaks),
                   peaks=[(round(a, 2), round(b, 2)) for a, b, _ in peaks], phones=inside)
        if expected is not None and i < len(expected):
            row["expected"] = expected[i]
            row["ok"] = len(peaks) == expected[i]
        report.append(row)
    return dict(segments=report, all_peaks=pk, phones=ph)


# ------------------------------------------------------------------ stems 回對原檔

def find_regions(x, sr, min_gap=0.02, min_len=0.05):
    """以連續數位零當 region 邊界（DAW 匯出的 stems 間隙是純零）。回傳 [(start, end)]。"""
    m = to_mono(x)
    nz = np.abs(m) > 1e-6
    if not nz.any():
        return []
    idx = np.flatnonzero(nz)
    cut = np.flatnonzero(np.diff(idx) > int(min_gap * sr))
    starts = np.concatenate([[idx[0]], idx[cut + 1]])
    ends = np.concatenate([idx[cut], [idx[-1]]]) + 1
    return [(s / sr, e / sr) for s, e in zip(starts, ends) if (e - s) / sr >= min_len]


def ncc_best(seg, src):
    """seg 在 src 內滑動的正規化交叉相關：回傳 (最大值, 位置樣本)。只用在非週期性素材（語音、噪音）。"""
    L = len(seg)
    if L > len(src):
        return 0.0, 0
    seg_n = seg - seg.mean()
    norm = np.linalg.norm(seg_n)
    if norm < 1e-9:
        return 0.0, 0
    corr = fftconvolve(src, seg_n[::-1], mode="valid")
    cs2 = np.concatenate([[0.0], np.cumsum(src.astype("float64") ** 2)])
    denom = np.sqrt(np.maximum(cs2[L:] - cs2[:-L], 1e-12)) * norm
    ncc = corr / denom
    k = int(np.argmax(ncc))
    return float(ncc[k]), k


def match_stems(stem_paths, source_paths, work_sr=11025, sub_win_s=1.0, low_score=0.9):
    """每個 stem 的每個 region 比對回來源檔，回傳 list of dict（start、end、source、src_start、ncc、pieces）。
    低分且長的 region 再用 1 秒視窗逐段比對，位移跳掉就是多段原檔拼接。"""
    from .io import load
    sources = {os.path.basename(p): load(p, sr=work_sr, mono=True)[0] for p in source_paths}
    out = []
    for sp in stem_paths:
        x, sr = load(sp, mono=True)
        regs = find_regions(x, sr)
        xw = load(sp, sr=work_sr, mono=True)[0]
        for t0, t1 in regs:
            seg = xw[int(t0 * work_sr):int(t1 * work_sr)]
            scores = {n: ncc_best(seg, s) for n, s in sources.items()}
            name = max(scores, key=lambda n: scores[n][0])
            sc, k = scores[name]
            pieces = []
            if sc < low_score and (t1 - t0) > 1.5:
                src = sources[name]
                win, hop = int(sub_win_s * work_sr), int(sub_win_s * work_sr / 2)
                sub = [(t0 + a / work_sr, ncc_best(seg[a:a + win], src)) for a in range(0, len(seg) - win, hop)]
                run = []
                for (ta, (sa, ka)) in sub:
                    if run and sa >= 0.6 and abs((ka / work_sr - run[-1][1]) - (ta - run[-1][0])) < 0.08:
                        run.append((ta, ka / work_sr))
                    else:
                        if len(run) >= 1 and run[0] is not None:
                            pieces.append((run[0][0], run[-1][0] + sub_win_s, run[0][1], run[-1][1] + sub_win_s))
                        run = [(ta, ka / work_sr)] if sa >= 0.6 else []
                if run:
                    pieces.append((run[0][0], run[-1][0] + sub_win_s, run[0][1], run[-1][1] + sub_win_s))
            out.append(dict(stem=os.path.basename(sp), start=round(t0, 3), end=round(t1, 3), source=name,
                            src_start=round(k / work_sr, 3), ncc=round(sc, 3),
                            pieces=[tuple(round(v, 2) for v in p) for p in pieces] if len(pieces) >= 2 else []))
    return out
