#!/usr/bin/env python3
"""
把子翎的音量 automation 從 stems_fx / stems_dry 的比值還原出來。
fx = dry × 增益曲線（外加溫和的 Comp／Chan EQ），所以逐視窗算 RMS 比值就是她的 volume 曲線。

輸出：
  automation_curves.png   六軌增益曲線（dB 對專案時間），只畫 region 有聲音的地方
  automation_curves.csv   time_s, track, gain_db（每 0.1 s 一點；乾版靜音處不輸出）

用法：python extract_automation.py <分軌資料夾>
"""
import csv
import sys
from pathlib import Path

import numpy as np
import soundfile as sf

ROOT = Path(sys.argv[1]).expanduser()
HOP_S = 0.1


def db(x):
    return 20 * np.log10(np.maximum(x, 1e-12))


def main():
    rows = []
    curves = {}
    for dry_path in sorted((ROOT / "stems_dry").glob("*.wav")):
        name = dry_path.stem
        d, fs = sf.read(str(dry_path), dtype="float32", always_2d=True)
        d = d[:, 0]
        x, _ = sf.read(str(ROOT / "stems_fx" / dry_path.name), dtype="float32", always_2d=True)
        m = x.mean(axis=1)
        n = min(len(d), len(m))
        d, m = d[:n], m[:n]
        hop = int(HOP_S * fs)
        ts, gs = [], []
        for i in range(0, n - hop, hop):
            a = d[i:i + hop]
            b = m[i:i + hop]
            ea = np.sqrt((a ** 2).mean())
            if ea < 1e-5:  # 乾版這裡沒聲音（region 之間），沒東西可比
                ts.append(i / fs); gs.append(np.nan)
                continue
            g = db(np.sqrt((b ** 2).mean()) / ea)
            ts.append(i / fs); gs.append(g)
            rows.append((round(i / fs, 2), name, round(float(g), 2)))
        curves[name] = (np.array(ts), np.array(gs))

    with open(ROOT / "automation_curves.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["time_s", "track", "gain_db"])
        w.writerows(rows)

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib import font_manager
    for cand in ["PingFang TC", "Heiti TC", "Hiragino Sans", "Arial Unicode MS"]:
        if any(f.name == cand for f in font_manager.fontManager.ttflist):
            plt.rcParams["font.family"] = cand
            break
    plt.rcParams["axes.unicode_minus"] = False

    total = max(t[-1] for t, _ in curves.values())
    fig, axes = plt.subplots(len(curves), 1, figsize=(18, 2.2 * len(curves)), sharex=True)
    for ax, (name, (t, g)) in zip(axes, curves.items()):
        ax.plot(t, g, lw=1.2, color="#3d405b")
        ax.fill_between(t, -40, g, where=~np.isnan(g), alpha=0.15, color="#3d405b")
        ax.set_ylim(-36, 3)
        ax.set_ylabel("dB")
        ax.set_title(name, loc="left", fontsize=10)
        ax.grid(alpha=0.3)
        ax.axhline(0, color="k", lw=0.5)
    ticks = np.arange(0, total + 1, 15)
    axes[-1].set_xticks(ticks)
    axes[-1].set_xticklabels([f"{int(s // 60)}:{s % 60:04.1f}" for s in ticks], fontsize=8)
    axes[-1].set_xlabel("專案時間")
    fig.suptitle("子翎的音量 automation（fx ÷ dry，每 0.1 s 的 RMS 比值；空白處是乾版沒聲音）", fontsize=12)
    fig.tight_layout()
    fig.savefig(ROOT / "automation_curves.png", dpi=150)

    for name, (t, g) in curves.items():
        v = g[~np.isnan(g)]
        print(f"{name}: 點數 {len(v)}，min {v.min():+.1f}  median {np.median(v):+.1f}  max {v.max():+.1f} dB")


if __name__ == "__main__":
    main()
