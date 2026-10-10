#!/usr/bin/env python
"""
輸出可供自行剪輯的素材層（stems）：
  00_素材切段/  小星星三句與完整主題的原始立體聲切段；三人 × 11 段注音分段（乾淨、只做音量統一與淡入淡出）
  03_素材層/    小星星五聲部「漂移 → 重同步 → 乾淨」各聲部單軌；低八度慢速聲部；ㄅㄆㄇㄈ 四聲部 phase loop
"""
import os, math, json, sys
import numpy as np, soundfile as sf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_effects as R      # 讀取小星星、提供 ou_drift / return_to_zero / render_voice / cut

SRC = R.SRC
OUT = R.OUT
CUTS = os.path.join(OUT, "00_素材切段"); STEMS = os.path.join(OUT, "03_素材層")
os.makedirs(os.path.join(CUTS, "注音分段_三人各十一段"), exist_ok=True); os.makedirs(STEMS, exist_ok=True)
made = []

def write(path, data, sr, note):
    if data.ndim == 1: data = data[:, None]
    peak = np.abs(data).max()
    if peak > 10 ** (-1 / 20): data = data / peak * 10 ** (-1 / 20)
    sf.write(path, data, sr, subtype="PCM_24"); made.append((os.path.relpath(path, OUT), len(data) / sr, note))
    print("wrote", os.path.relpath(path, OUT), f"{len(data)/sr:.1f}s")

# ---------------------------------------------------------------- 小星星原始立體聲切段
st, sr1 = sf.read(os.path.join(SRC, "中藥行小星星.wav"), always_2d=True)
def cut_st(t0, t1, fade=0.012):
    seg = st[int(round(t0 * sr1)):int(round(t1 * sr1))].copy(); n = int(fade * sr1); w = np.linspace(0, 1, n)[:, None]
    seg[:n] *= w; seg[-n:] *= w[::-1]; return seg
write(os.path.join(CUTS, "小星星_第一句_0.52-19.90s_原始.wav"), cut_st(0.52, 19.90), sr1, "一閃一閃亮晶晶、滿天都是小星星。可無縫循環。")
write(os.path.join(CUTS, "小星星_第二句_19.90-28.79s_原始.wav"), cut_st(19.90, 28.79), sr1, "掛在天上放光明")
write(os.path.join(CUTS, "小星星_第三句_28.79-37.95s_原始.wav"), cut_st(28.79, 37.95), sr1, "好像許多小眼睛")
write(os.path.join(CUTS, "小星星_完整主題_三句_0.52-37.95s_原始.wav"), cut_st(0.52, 37.95), sr1, "前奏完整主題，未加任何效果，可當結尾的純淨版")

# ---------------------------------------------------------------- 注音分段（三人 × 11 段）
GJ = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "bpmf_groups.json")))
GROUPS = GJ["order"]
for name, f in [("阿瑤", "阿瑤ㄅㄆㄇ.wav"), ("柏豪", "柏豪ㄅㄆㄇ.wav"), ("小軒", "小軒ㄅㄆㄇ.wav")]:
    y, sr2 = sf.read(os.path.join(SRC, f), always_2d=True); y = y.mean(axis=1)
    for gi, g in enumerate(GROUPS):
        a0, b0 = GJ["spans"][name][g]
        seg = y[int(a0 * sr2):int(b0 * sr2)].copy(); n = int(0.012 * sr2); w = np.linspace(0, 1, n)
        seg[:n] *= w; seg[-n:] *= w[::-1]; seg = seg / (np.sqrt(np.mean(seg ** 2)) + 1e-9) * 0.08
        write(os.path.join(CUTS, "注音分段_三人各十一段", f"{name}_{gi+1:02d}_{g}.wav"), seg, sr2, f"{name} {g}（{a0:.2f}–{b0:.2f} s）")

# ---------------------------------------------------------------- 小星星五聲部 漂移 → 重同步 → 乾淨（各聲部單軌）
sr = R.SR1; A = R.A; LA = R.LA
dur = 100; n_out, n_ctrl, t_ctrl = R.timeline(dur, sr)
rng = np.random.default_rng(3); env = R.grow_env(t_ctrl, 8, 40)
t_sync, tau = 58.0, 2.5; grid = LA / 2
n_r = R.grid_reset_index(t_sync + 3.5 * tau, grid, sr)
for i in range(5):
    d = R.ou_drift(n_ctrl, 1 / R.CTRL_HZ, sigma_cents=7.0, theta=0.03, max_dev=18, rng=rng, env=env)
    d = R.return_to_zero(d, t_ctrl, t_sync, tau)
    rate = R.cents_to_rate(R.to_audio_rate(d, t_ctrl, n_out, sr))
    v, _ = R.render_voice(A, rate, resets=[n_r], sr=sr)
    write(os.path.join(STEMS, f"小星星_第一句_聲部{i+1}_漂移58s重同步_{n_r/sr:.1f}s起乾淨.wav"), v * 0.9, sr,
          f"聲部 {i+1}：0–8 s 原速，之後 random walk 漂移（上限 ±18 cents），58 s 起滑回原速，{n_r/sr:.1f} s 硬對齊句首，之後為原速乾淨循環到 100 s。五軌同時播放即 03 號示範，各自音量與 pan 可自行決定。")
# 低八度慢速聲部（rate 0.5，帶輕微漂移，無濾波）
d = R.ou_drift(n_ctrl, 1 / R.CTRL_HZ, sigma_cents=4.0, theta=0.04, max_dev=10, rng=np.random.default_rng(11), env=env)
d = R.return_to_zero(d, t_ctrl, t_sync, tau)
rate = 0.5 * R.cents_to_rate(R.to_audio_rate(d, t_ctrl, n_out, sr))
v, _ = R.render_voice(A, rate, resets=[n_r], sr=sr)
write(os.path.join(STEMS, "小星星_第一句_低八度半速聲部_漂移58s重同步.wav"), v * 0.9, sr, "rate 0.5：低八度、兩倍長，漂移與重同步時程同上，可墊在五聲部下面。")

# ---------------------------------------------------------------- ㄅㄆㄇㄈ 四聲部 phase loop（乾淨、無殘響）
bh, sr2 = sf.read(os.path.join(SRC, "柏豪ㄅㄆㄇ.wav"), always_2d=True); bh = bh.mean(axis=1)
BPMF = R.cut(bh, sr2, 0.10, 2.45)
dur8 = 60; n8 = int(dur8 * sr2); t8 = np.arange(n8) / sr2
t_sync8, tau8 = 40.0, 2.0; LB = len(BPMF) / sr2
n_r8 = R.grid_reset_index(t_sync8 + 3.5 * tau8, LB, sr2)
voices = []
for i, c in enumerate([0, 6, -6, 12]):
    cents = np.full(n8, float(c)); cents[t8 < 4] = 0; m = t8 >= t_sync8; cents[m] = c * np.exp(-(t8[m] - t_sync8) / tau8)
    v, _ = R.render_voice(BPMF, R.cents_to_rate(cents), resets=[n_r8], sr=sr2); voices.append(v)
    write(os.path.join(STEMS, f"ㄅㄆㄇㄈ_柏豪_phase聲部{i+1}_{c:+d}cents_40s重同步.wav"), v * 0.8, sr2, f"柏豪「ㄅㄆㄇㄈ」2.35 s 循環，偏移 {c:+d} cents，40 s 起收回，{n_r8/sr2:.1f} s 對齊。")

json.dump(made, open(os.path.join(OUT, "_stems_manifest.json"), "w"), ensure_ascii=False, indent=0)
print("done", len(made), "files")
