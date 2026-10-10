"""驗證 out_pads 並產生試聽檔。用法：python verify_and_previews.py out_pads 試聽輸出夾"""
import sys, json, pathlib, numpy as np, soundfile as sf, librosa
SR = 44100
OUT = pathlib.Path(sys.argv[1]); PRE = pathlib.Path(sys.argv[2]); PRE.mkdir(exist_ok=True)
meta = json.load(open(OUT / "render_meta.json"))
def rms(x): return np.sqrt(np.mean(x ** 2))
W = SR // 2   # 0.5 秒窗
print(f"{'file':46s} {'len':>7s} {'loop@':>6s} {'seam':>7s} {'1s-RMS min/max vs median':>26s} {'onset':>6s}")
for name, info in meta["files"].items():
    x, _ = sf.read(OUT / name, always_2d=True); m = x.mean(1); n = len(m); ls = info["live_loop_start_s"]
    if ls is None: print(f"{name:46s} {n/SR:6.1f}s one-shot"); continue
    L = int(ls * SR); loop = m[L:]
    env = np.array([rms(loop[i:i + SR]) for i in range(0, len(loop) - SR, SR)]); env_db = 20 * np.log10(env + 1e-12); med = np.median(env_db)
    seam_db = 20 * np.log10(rms(m[-W:]) / rms(m[L:L + W]))
    on = float(librosa.onset.onset_strength(y=loop[int(20 * SR):int(80 * SR)], sr=SR).mean())
    print(f"{name:46s} {n/SR:6.1f}s {ls:5.0f}s {seam_db:+6.1f}dB {env_db.min()-med:+10.1f}/{env_db.max()-med:+5.1f} dB {on:6.2f}")

# 試聽：第一幕 pad 疊 8/12 講話；第三幕 drone（打開狀態）疊 8/12 阿瑤 solo；各幕單獨
def mixdown(bed, pad, off_db, path):
    g = 10 ** (off_db / 20) * rms(bed) / rms(pad); mix = bed + pad * g
    mix = mix / max(1.0, np.max(np.abs(mix)) / 0.98); sf.write(path, mix, SR, subtype="PCM_16")
    return round(20 * np.log10(g), 1)
sp, _ = sf.read("speech_0812_0055-0250.wav", always_2d=True)
p1, _ = sf.read(OUT / "01_第一幕_主音pad_head8s.wav", always_2d=True); p1 = p1[8 * SR: 8 * SR + len(sp)]
for off in (-22, -16): mixdown(sp, p1, off, PRE / f"試聽_第一幕pad疊講話_{abs(off)}dB下.wav")
solo, _ = sf.read("solo_0812_0815-1045.wav", always_2d=True)
p3, _ = sf.read(OUT / "03A_第三幕_drone_立即進入_head8s.wav", always_2d=True)
L3 = int(meta["files"]["03A_第三幕_drone_立即進入_head8s.wav"]["live_loop_start_s"] * SR)
p3open = np.tile(p3[L3:], (3, 1))[: len(solo)]
for off in (-18, -12): mixdown(solo, p3open, off, PRE / f"試聽_第三幕drone疊solo_{abs(off)}dB下.wav")
p3c, _ = sf.read(OUT / "03C_第三幕_顆粒版_立即進入_head8s.wav", always_2d=True)
L3c = int(meta["files"]["03C_第三幕_顆粒版_立即進入_head8s.wav"]["live_loop_start_s"] * SR)
p3c_open = np.tile(p3c[L3c:], (3, 1))[: len(solo)]
mixdown(solo, p3c_open, -18, PRE / "試聽_第三幕顆粒版疊solo_18dB下.wav")
sf.write(PRE / "試聽_第三幕顆粒版打開狀態_單獨_60s.wav", p3c_open[:60 * SR] * 0.5, SR, subtype="PCM_16")
sf.write(PRE / "試聽_第三幕顆粒版_關閉到打開_190s-300s.wav", p3c[190 * SR:300 * SR] * 0.5, SR, subtype="PCM_16")
p2, _ = sf.read(OUT / "02_第二幕_空五度pad_head8s.wav", always_2d=True)
sf.write(PRE / "試聽_第一幕pad單獨_60s.wav", p1[:60 * SR] * 0.5, SR, subtype="PCM_16")
sf.write(PRE / "試聽_第二幕pad單獨_60s.wav", p2[8 * SR:68 * SR] * 0.5, SR, subtype="PCM_16")
sf.write(PRE / "試聽_第三幕drone打開狀態_單獨_60s.wav", p3open[:60 * SR] * 0.5, SR, subtype="PCM_16")
sf.write(PRE / "試聽_第三幕drone_關閉到打開_190s-300s.wav", p3[190 * SR:300 * SR] * 0.5, SR, subtype="PCM_16")
print("previews written to", PRE)
