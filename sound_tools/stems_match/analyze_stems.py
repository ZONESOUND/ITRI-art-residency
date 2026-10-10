#!/usr/bin/env python3
"""
分析 Logic Pro 匯出的乾版 stems（stems_dry/），找出每軌的 region 起迄，
用正規化交叉相關比對回 GarageBand 專案的原始素材，標出每段取自原檔哪一秒，
再對照注音十一段邊界、小星星樂句邊界、朗讀轉錄，產生：

  timeline_data.json   所有 region 與標籤（機器可讀）
  timeline_tables.md   軌道總表、時間軸表（貼進 README）
  timeline.png         六軌 region 條圖

用法：python analyze_stems.py <分軌資料夾> [whisper_out 資料夾]
"""
import json
import sys
from pathlib import Path

import numpy as np
import soundfile as sf
from scipy.signal import resample_poly, fftconvolve

ROOT = Path(sys.argv[1]).expanduser()
WHISPER_DIR = Path(sys.argv[2]).expanduser() if len(sys.argv) > 2 else None
STEMS = ROOT / "stems_dry"
SRC_DIR = ROOT / "原始專案_子翎" / "小星星二版 9.3.band" / "Media" / "Audio Files"
BPMF_JSON = ROOT.parent / "效果測試_20260902" / "scripts" / "bpmf_groups.json"

FS_WORK = 11025  # 交叉相關用的取樣率（44100 / 4）

# 來源素材：檔名 → (人, 類型)。_1 檔與無 _1 檔位元相同，只留一份當候選。
SOURCES = {
    "中藥行小星星.wav": ("中藥行", "小星星"),
    "小軒ㄅㄆㄇ.wav": ("小軒", "ㄅㄆㄇ"),
    "小軒朗讀.wav": ("小軒", "朗讀"),
    "柏成朗讀.wav": ("柏成", "朗讀"),
    "柏豪ㄅㄆㄇ_1.wav": ("柏豪", "ㄅㄆㄇ"),
    "阿瑤ㄅㄆㄇ_1.wav": ("阿瑤", "ㄅㄆㄇ"),
    "阿瑤朗讀.wav": ("阿瑤", "朗讀"),
}

# whisper 會吐簡體與英文字母，對回繁體與注音（字母對注音是依劇本「ㄅ寶貝／ㄆ朋友／ㄇ媽媽／ㄈ飛翔」的推定，標記時仍屬機器轉錄）
S2T = str.maketrans("宝贝梦妈饼干们吗当师环游见试毕业飞来没关系远", "寶貝夢媽餅乾們嗎當師環遊見試畢業飛來沒關係遠")
LETTER2BPMF = {"B": "ㄅ", "P": "ㄆ", "M": "ㄇ", "F": "ㄈ", "啵": "[unclear: 啵＝ㄅ?]", "摸": "[unclear: 摸＝ㄇ?]"}

# 小星星前奏三句的樂句邊界（效果測試_20260902/README.md，音高追蹤抓的）
STAR_PHRASES = [
    (0.52, 19.90, "第一句：一閃一閃亮晶晶、滿天都是小星星"),
    (19.90, 28.79, "第二句：掛在天上放光明"),
    (28.79, 37.95, "第三句：好像許多小眼睛"),
]


def load_mono(path, fs_target=None):
    x, fs = sf.read(str(path), dtype="float32", always_2d=True)
    x = x.mean(axis=1)
    if fs_target and fs != fs_target:
        g = np.gcd(fs, fs_target)
        x = resample_poly(x, fs_target // g, fs // g).astype("float32")
        fs = fs_target
    return x, fs


def find_regions(x, fs, min_gap=0.02, min_len=0.05):
    """以「連續零樣本」當 region 邊界（Logic 匯出的 region 間隙是純數位零）。"""
    nz = np.abs(x) > 1e-6
    if not nz.any():
        return []
    idx = np.flatnonzero(nz)
    gaps = np.diff(idx)
    cut = np.flatnonzero(gaps > int(min_gap * fs))
    starts = np.concatenate([[idx[0]], idx[cut + 1]])
    ends = np.concatenate([idx[cut], [idx[-1]]]) + 1
    regs = [(s / fs, e / fs) for s, e in zip(starts, ends) if (e - s) / fs >= min_len]
    return regs


def ncc_best(seg, src):
    """seg 在 src 內滑動的正規化交叉相關最大值與位置（樣本）。"""
    L = len(seg)
    if L > len(src):
        return 0.0, 0
    seg_n = seg - seg.mean()
    seg_norm = np.linalg.norm(seg_n)
    if seg_norm < 1e-9:
        return 0.0, 0
    corr = fftconvolve(src, seg_n[::-1], mode="valid")
    # 滑動視窗的能量（去均值近似：用能量即可，seg 已去均值）
    cs2 = np.concatenate([[0.0], np.cumsum(src.astype("float64") ** 2)])
    win_e = cs2[L:] - cs2[:-L]
    denom = np.sqrt(np.maximum(win_e, 1e-12)) * seg_norm
    ncc = corr / denom
    k = int(np.argmax(ncc))
    return float(ncc[k]), k


def fmt(t):
    m = int(t // 60)
    s = t - 60 * m
    return f"{m}:{s:05.2f}"


def main():
    bpmf = json.loads(BPMF_JSON.read_text(encoding="utf-8"))
    sources = {}
    for name in SOURCES:
        x, _ = load_mono(SRC_DIR / name, FS_WORK)
        sources[name] = x

    whisper = {}
    if WHISPER_DIR and WHISPER_DIR.exists():
        for jf in WHISPER_DIR.glob("*.json"):
            d = json.loads(jf.read_text(encoding="utf-8"))
            words = []
            for seg in d.get("segments", []):
                # whisper 幻覺迴圈的特徵：一串長度 0 的詞；整段丟掉
                ws = seg.get("words", [])
                zero = sum(1 for w in ws if float(w["end"]) - float(w["start"]) < 0.02)
                if ws and zero / len(ws) > 0.3:
                    continue
                for w in ws:
                    t0, t1 = float(w["start"]), float(w["end"])
                    txt = w["word"].strip().rstrip(",，。?？!！")
                    if t1 - t0 < 0.05 or not txt or txt == "-":
                        continue
                    txt = txt.translate(S2T)
                    txt = LETTER2BPMF.get(txt, txt)
                    words.append((t0, t1, txt, float(w.get("probability", 0))))
            whisper[jf.stem] = words

    tracks = []
    for stem_path in sorted(STEMS.glob("*.wav")):
        x44, fs44 = load_mono(stem_path)
        regs = find_regions(x44, fs44)
        xw = resample_poly(x44, 1, 4).astype("float32")
        entries = []
        for (t0, t1) in regs:
            seg = xw[int(t0 * FS_WORK): int(t1 * FS_WORK)]
            best = None
            scores = {}
            for name, src in sources.items():
                sc, k = ncc_best(seg, src)
                scores[name] = sc
                if best is None or sc > best[0]:
                    best = (sc, k, name)
            sc, k, name = best
            second = sorted(scores.values(), reverse=True)[1]
            person, kind = SOURCES[name]
            src_t0 = k / FS_WORK
            src_t1 = src_t0 + (t1 - t0)
            # 低分 region：用 1 秒視窗逐段比對，看是不是好幾段原檔拼起來的
            sub = []
            if sc < 0.9 and (t1 - t0) > 1.5:
                src = sources[name]
                win = int(1.0 * FS_WORK); hop = int(0.5 * FS_WORK)
                for a in range(0, len(seg) - win, hop):
                    s2, k2 = ncc_best(seg[a:a + win], src)
                    sub.append((round(t0 + a / FS_WORK, 2), round(k2 / FS_WORK, 2), round(s2, 2)))
            # 把子視窗的原檔位移分成「連續的段」：位移隨時間等速前進就是同一段，跳掉就是拼接
            pieces = []  # (region_t0, region_t1, src_t0, src_t1)
            if sub:
                run = [sub[0]]
                for prev, cur in zip(sub, sub[1:]):
                    if cur[2] >= 0.6 and prev[2] >= 0.6 and abs((cur[1] - prev[1]) - (cur[0] - prev[0])) < 0.08:
                        run.append(cur)
                    else:
                        if run[0][2] >= 0.6:
                            pieces.append((run[0][0], run[-1][0] + 1.0, run[0][1], run[-1][1] + 1.0))
                        run = [cur]
                if run[0][2] >= 0.6:
                    pieces.append((run[0][0], run[-1][0] + 1.0, run[0][1], run[-1][1] + 1.0))
                # 相鄰兩段之間若有空隙（轉場視窗分數低），前一段的結尾接到下一段的開頭
                for i in range(len(pieces) - 1):
                    p, q = pieces[i], pieces[i + 1]
                    if p[1] < q[0]:
                        pieces[i] = (p[0], q[0], p[2], p[2] + (q[0] - p[0]))
                # 最後一段延伸到 region 結尾
                if pieces and pieces[-1][1] < t1:
                    p = pieces[-1]; pieces[-1] = (p[0], t1, p[2], p[2] + (t1 - p[0]))
            composite = len(pieces) >= 2
            spans = [(p[2], p[3]) for p in pieces] if composite else [(src_t0, src_t1)]

            def label_span(a0, a1):
                out = []
                if kind == "ㄅㄆㄇ":
                    for grp, (a, b) in bpmf["spans"][person].items():
                        if min(b, a1) - max(a, a0) > 0.15:
                            out.append(grp)
                elif kind == "小星星":
                    for a, b, txt in STAR_PHRASES:
                        if min(b, a1) - max(a, a0) > 0.5:
                            out.append(txt)
                    if a1 > STAR_PHRASES[-1][1] + 0.5:
                        out.append(f"37.95 s 之後（前奏三句以外，未標記樂句，至 {a1:.1f} s）")
                elif kind == "朗讀":
                    key = name.replace(".wav", "")
                    for (a, b, w, p) in whisper.get(key, []):
                        # 詞要有一半以上（至少 0.15 s）落在這段裡才算，避免邊界上的詞被算兩次
                        if min(b, a1) - max(a, a0) > max(0.15, 0.5 * (b - a)):
                            out.append(w if (p >= 0.5 or w.startswith("[unclear")) else f"[unclear: {w}]")
                return out

            labels = []
            for (a0, a1) in spans:
                lab = label_span(a0, a1)
                if composite:
                    labels.append(f"〔原檔 {a0:.2f}–{a1:.2f} s〕" + "、".join(lab))
                else:
                    labels.extend(lab)
            entries.append({
                "composite_pieces": [dict(zip(("start", "end", "src_start", "src_end"), map(lambda v: round(v, 2), p))) for p in pieces] if composite else [],
                "start": round(t0, 3), "end": round(t1, 3), "dur": round(t1 - t0, 3),
                "source": name, "person": person, "kind": kind,
                "src_start": round(src_t0, 3), "src_end": round(src_t1, 3),
                "ncc": round(sc, 3), "ncc_second": round(second, 3),
                "labels": labels,
                "unclear": sc < 0.6 and not composite,
                "sub_windows": sub,
            })
        tracks.append({"file": stem_path.name, "length": round(len(x44) / fs44, 3), "regions": entries})

    (ROOT / "timeline_data.json").write_text(json.dumps(tracks, ensure_ascii=False, indent=1), encoding="utf-8")

    # ---- markdown 表 ----
    md = []
    md.append("## 軌道總表\n")
    md.append("| Logic 軌名 | 主要來源 | 人 | 類型 | region 數 | 內容時間範圍 | 乾版長度 |")
    md.append("|---|---|---|---|---|---|---|")
    for tr in tracks:
        if not tr["regions"]:
            md.append(f"| {tr['file']} | （空軌） | | | 0 | | {tr['length']} s |")
            continue
        srcs = {}
        for r in tr["regions"]:
            srcs[r["source"]] = srcs.get(r["source"], 0) + r["dur"]
        main_src = max(srcs, key=srcs.get)
        person, kind = SOURCES[main_src]
        extra = "" if len(srcs) == 1 else "（另含 " + "、".join(s for s in srcs if s != main_src) + "）"
        t0 = tr["regions"][0]["start"]; t1 = tr["regions"][-1]["end"]
        md.append(f"| {tr['file']} | {main_src}{extra} | {person} | {kind} | {len(tr['regions'])} | {fmt(t0)}–{fmt(t1)} | {tr['length']} s |")

    md.append("\n## 時間軸表（依專案時間排序）\n")
    md.append("| 專案時間 | 長度 | 軌 | 人 | 內容 | 取自原檔秒數 | 比對分數 |")
    md.append("|---|---|---|---|---|---|---|")
    allr = []
    for tr in tracks:
        for r in tr["regions"]:
            allr.append((r["start"], tr["file"], r))
    allr.sort(key=lambda t: t[0])
    for t0, f, r in allr:
        lab = "、".join(r["labels"]) if r["labels"] else "（未對到標籤）"
        if r["unclear"]:
            lab = f"[unclear: 比對分數低] {lab}"
        if r["composite_pieces"]:
            srcpos = "拼接：" + " ＋ ".join(f"{p['src_start']:.2f}–{p['src_end']:.2f}" for p in r["composite_pieces"]) + " s"
            lab = "（兩段以上原檔拼成一個 region）" + lab
        else:
            srcpos = f"{r['src_start']:.2f}–{r['src_end']:.2f} s"
        md.append(f"| {fmt(r['start'])}–{fmt(r['end'])} | {r['dur']:.2f} s | {f.replace('.wav','')} | {r['person']} | {r['kind']}：{lab} | {r['source'].replace('.wav','')} {srcpos} | {r['ncc']:.2f} |")
    (ROOT / "timeline_tables.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    # ---- 圖 ----
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib import font_manager
    for cand in ["PingFang TC", "Heiti TC", "Hiragino Sans", "Arial Unicode MS"]:
        if any(f.name == cand for f in font_manager.fontManager.ttflist):
            plt.rcParams["font.family"] = cand
            break
    plt.rcParams["axes.unicode_minus"] = False
    colors = {"ㄅㄆㄇ": "#e07a5f", "朗讀": "#3d405b", "小星星": "#81b29a"}
    fig, ax = plt.subplots(figsize=(18, 6))
    total = max(tr["length"] for tr in tracks)
    for i, tr in enumerate(tracks):
        y = len(tracks) - i
        for r in tr["regions"]:
            ax.broken_barh([(r["start"], r["dur"])], (y - 0.35, 0.7), color=colors[r["kind"]], alpha=0.9)
        srcs = {r["source"] for r in tr["regions"]}
        ax.text(-2, y, f"{tr['file'].replace('.wav','')}\n" + "／".join(s.replace('.wav','') for s in sorted(srcs)), ha="right", va="center", fontsize=8)
    ax.set_xlim(0, total + 2)
    ax.set_ylim(0.3, len(tracks) + 0.7)
    ax.set_yticks([])
    ax.set_xlabel("專案時間（秒）")
    ticks = np.arange(0, total + 1, 15)
    ax.set_xticks(ticks)
    ax.set_xticklabels([fmt(t) for t in ticks], fontsize=8)
    ax.grid(axis="x", alpha=0.3)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=c, label=k) for k, c in colors.items()], loc="upper right")
    ax.set_title("小星星二版 9.3（子翎 GarageBand）六軌 region 時間軸")
    fig.tight_layout()
    fig.savefig(ROOT / "timeline.png", dpi=150)

    # 摘要印到終端
    for tr in tracks:
        print(tr["file"], tr["length"], "s,", len(tr["regions"]), "regions")
        for r in tr["regions"]:
            print(f"   {fmt(r['start'])}-{fmt(r['end'])}  {r['source']:<16} src {r['src_start']:7.2f}-{r['src_end']:7.2f}  ncc {r['ncc']:.2f}/{r['ncc_second']:.2f}  {'、'.join(r['labels'])[:60]}")
            for (pt, st, s2) in r["sub_windows"]:
                print(f"        sub @{pt:7.2f} -> src {st:7.2f}  ncc {s2:.2f}")


if __name__ == "__main__":
    main()
