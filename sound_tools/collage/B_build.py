"""
B_build.py：《節奏繞纏》第四幕旅行拼貼，代號 B「永遠在路上」。
穩態層疊，四層永遠同時存在，只在層內輪換素材；頭尾可無縫循環。
用法：在 scratchpad 目錄 `source .venv/bin/activate && python agent_B/B_build.py`
輸出：{ROOT}/旅行移動素材/拼貼試做_20260915/B_永遠在路上_{D}s.wav（+ mp3）
同時把 cue 表與量測數字寫到 agent_B/B_cues.json 供設計說明引用。
"""
import os, sys, json, math, shutil
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import collage_lib as L

SR = L.SR
D = 168.0          # 成品長度（秒）
XF = 8.0           # 頭尾折疊交叉淡化長度（秒）：連續層建成 D+XF，再把尾端 XF 折回開頭
SEED = 20260915
TITLE = "永遠在路上"
OUT_DIR = os.path.join(L.TRAVEL, "拼貼試做_20260915")
RV = dict(rt60=2.4, lp_hz=4000, predelay_ms=20)   # 整支檔唯一一組殘響
RV_MIX = 0.28
T = L.TRAVEL
R = L.ROOT
rng = np.random.default_rng(SEED)
cues = {"floor": [], "transport": [], "events": [], "body": [], "memory": []}

def src(rel):
    return os.path.join(T, rel)

def fold(x, dur=D, xf=XF):
    """把長度 D+XF 的層折成 D：尾端 XF 秒等功率交叉淡化到開頭，讓 D→0 的接縫連續。"""
    n, k = int(dur * SR), int(xf * SR)
    x = L.stereo(x)
    out = x[:n].copy()
    tail = x[n:n + k]
    m = len(tail)
    r = np.linspace(0, 1, m)
    a, b = np.sin(r * math.pi / 2)[:, None], np.cos(r * math.pi / 2)[:, None]
    out[:m] = out[:m] * a + tail * b
    return out

def place_wrap(bus, seg, t, gain_db=0.0, pan=0.0):
    """place，但超出 D 的部分繞回開頭（讓循環時事件的尾巴也接得起來）。"""
    n = len(bus)
    seg = L.stereo(seg)
    L.place(bus, seg, t, gain_db, pan)
    over = int(t * SR) + len(seg) - n
    if over > 0:
        L.place(bus, seg[len(seg) - over:], 0.0, gain_db, pan)

def tame(x, thresh_db=-26.0, ratio=4.0):
    """快速壓縮（attack 2 ms、release 120 ms）：專門削 50 ms 尺度的撞擊與起音，慢速電平器管不到的部分。"""
    x = L.norm_lufs(x, -20)
    x = L._compress(x, thresh_db=thresh_db, ratio=ratio, attack_s=0.002, release_s=0.12)
    return L.norm_lufs(x, -20)

def prep_cont(rel, a, b, lp=7000, lev=(2.0, 8.0)):
    """連續素材：剪 a..b 秒 → norm −20 → 慢速電平器壓平 → 低通 → 再 norm。"""
    x = L.cut(L.load(src(rel)), a, b)
    x = L.norm_lufs(x, -20)
    x = L.leveler(x, lev[0], lev[1])
    x = L.leveler(x, 0.4, 6.0)      # 再一道 0.4 s 的短電平器
    x = tame(x)                      # 快速壓縮：削掉亂流、火車的瞬間撞擊
    x = L.lowpass(x, lp)
    return L.norm_lufs(x, -20)

# ------------------------------------------------------------------ 1. 地板層（連續）
def build_floor():
    total = D + XF
    bus = L.timeline(total)
    # 兩支風以 56 秒為週期慢慢互換（等功率），三個週期剛好等於 D，循環時相位連續
    wind_a = L.loop_to(prep_cont("06_風與空氣/ParkWindBlowAmbience_BWU.57.wav", 2, 112, lp=5000), total, 4.0)
    wind_b = L.loop_to(prep_cont("06_風與空氣/ESM_Ocean_Loop_New_York_Wind_Waves_Distant_5_Deep.wav", 0, 68, lp=5000), total, 4.0)
    t = np.arange(int(total * SR)) / SR
    th = math.pi * t / 56.0
    ga, gb = np.abs(np.cos(th))[:, None], np.abs(np.sin(th))[:, None]
    L.place(bus, wind_a * ga, 0, -12.0, -0.2)
    L.place(bus, wind_b * gb, 0, -12.0, 0.2)
    waves = L.loop_to(prep_cont("04_水上與船/PirateShipOceanWaves_SFXB.1.wav", 100, 180, lp=5000), total, 5.0)
    L.place(bus, waves, 0, -14.0, 0.0)
    city = L.loop_to(prep_cont("03_道路與城市/CityStreet_BW.1723.wav", 55, 85, lp=4000), total, 3.0)
    L.place(bus, city, 0, -16.0, 0.0)
    cues["floor"] = [
        dict(file="06_風與空氣/ParkWindBlowAmbience_BWU.57.wav", cut="2–112 s，loop（接縫 4 s）", proc="norm −20、leveler 2 s/8 dB、低通 5 kHz、56 秒週期與另一支風等功率互換", gain_db=-12, pan=-0.2),
        dict(file="06_風與空氣/ESM_Ocean_Loop_New_York_Wind_Waves_Distant_5_Deep.wav", cut="0–68 s，loop（接縫 4 s）", proc="同上，與 ParkWind 互補相位", gain_db=-12, pan=0.2),
        dict(file="04_水上與船/PirateShipOceanWaves_SFXB.1.wav", cut="100–180 s，loop（接縫 5 s）", proc="norm −20、leveler 2 s/8 dB、低通 5 kHz", gain_db=-14, pan=0.0),
        dict(file="03_道路與城市/CityStreet_BW.1723.wav", cut="55–85 s，loop（接縫 3 s）", proc="norm −20、leveler 2 s/8 dB、低通 4 kHz", gain_db=-16, pan=0.0),
    ]
    return fold(bus)

# ------------------------------------------------------------------ 2. 交通層（連續、輪換，主層 0 dB）
TRANSPORT = [
    # 名稱、檔、可用區間 (a, b)、低通、是否需要短 loop
    ("地鐵車廂", "02_火車與地鐵/SubwayInterior_S08TT.6.wav", (12, 46), 7000, False),
    ("火車行進", "02_火車與地鐵/FF_MT_train_foley_journey_gentle.wav", (0.5, 28), 7000, False),
    ("倫敦地鐵隧道", "02_火車與地鐵/FF_CL_ambience_london_underground_northern_line_quiet_green.wav", (26, 44.5), 7000, False),
    ("船引擎", "04_水上與船/PontoonBoatMedium_BW.5320.M.wav", (1.0, 8.0), 6000, True),
    ("飛機艙內亂流", "01_飛機與機場/BRS_Plane_Turbulance_Hard_1.wav", (1.0, 21.0), 6000, False),
    ("公車站", "03_道路與城市/FF_CL_ambience_london_bus_station_red.wav", (0.0, 8.6), 7000, True),
    ("火車車廂空間", "02_火車與地鐵/FF_MT_train_foley_room_ambience.wav", (0.0, 18.0), 6000, False),
    ("機場大廳", "01_飛機與機場/PSE_GGV1_FX_One_Shot_Ambience_Tokyo_Airport_Departure_Lobby.wav", (2.0, 34.0), 7000, False),
    ("火車站月台", "02_火車與地鐵/TrainStation_BW.51897.wav", (1.0, 70.0), 7000, False),
]

def build_transport():
    total = D + XF
    # 固定 seed 的輪換順序：兩輪洗牌接起來，避免相鄰重複
    order = list(rng.permutation(len(TRANSPORT)))
    second = list(rng.permutation(len(TRANSPORT)))
    if second[0] == order[-1]:
        second.append(second.pop(0))
    order += second
    segs, xfs, pos, cur = [], [], 0.0, 0
    cache = {}
    while pos < total + 4:
        name, rel, (a, b), lp, need_loop = TRANSPORT[order[cur]]
        seg_len = float(rng.uniform(18, 30))
        xf = float(rng.uniform(6, 8))
        if rel not in cache:
            cache[rel] = prep_cont(rel, a, b, lp=lp, lev=(2.0, 8.0))
        base = cache[rel]
        avail = len(base) / SR
        if need_loop or avail < seg_len:
            seg = L.loop_to(base, seg_len, 2.0)
            cut_desc = f"{a}–{b} s 短 loop（接縫 2 s）到 {seg_len:.1f} s"
        else:
            off = float(rng.uniform(0, avail - seg_len))
            seg = L.cut(base, off, off + seg_len)
            cut_desc = f"{a + off:.1f}–{a + off + seg_len:.1f} s"
        start = pos - (xfs[-1] if xfs else 0)
        cues["transport"].append(dict(t=round(start, 1), name=name, file=rel, cut=cut_desc, seg_s=round(seg_len, 1),
                                      xfade_in_s=round(xfs[-1], 1) if xfs else 0.0, proc=f"norm −20、leveler 2 s/8 dB、低通 {lp} Hz", gain_db=0))
        segs.append(seg); xfs.append(xf)
        pos = start + seg_len
        cur += 1
        if cur >= len(order):
            order += list(rng.permutation(len(TRANSPORT)))
    y = L.xfade_concat(segs, xfs[:-1])
    y = y[:int(total * SR)]
    bus = L.timeline(total)
    L.place(bus, y, 0, 0.0, 0.0)
    return fold(bus)

# ------------------------------------------------------------------ 3. 事件層（間歇、規律呼吸週期，−4 dB）
EVENTS = [
    ("安全帶提示音", "01_飛機與機場/FF_MT_airplane_foley_seatbelt_sign_dry.wav", (0.0, 1.15), 3000),
    ("地鐵門開提示", "02_火車與地鐵/FF_MT_london_underground_foley_doors_open_low_beep.wav", (0.0, 3.0), 5000),
    ("行李箱輪子（中）", "01_飛機與機場/BRS_Wheels_Luggage_Bag_OB_Roll_Med.wav", (2.0, 4.8), 5000),
    ("行李箱輪子（慢）", "01_飛機與機場/BRS_Wheels_Luggage_Bag_OB_Roll_Slow.wav", (3.0, 6.0), 5000),
    ("方向燈三下", "03_道路與城市/CarTurnSignal_BW.62374.wav", (1.4, 4.7), 5000),
    ("腳步（水泥）", os.path.join(R, "腳步聲素材/FootstepsCement_BW.7554.wav"), (0.0, 2.6), 5000),
    ("腳步（碎石）", os.path.join(R, "腳步聲素材/FootstepsGravel_BW.7744.wav"), (0.0, 2.5), 5000),
    ("腳步（同根聲）", os.path.join(R, "腳步聲素材/2019同根聲_Footsteps.aif"), (0.5, 3.0), 5000),
    ("遠方汽笛", "02_火車與地鐵/TrainHornDist_SEU04.48.wav", (0.0, 4.2), 4000),
    ("划槳", "04_水上與船/FF_MC_foley_paddling_sea_kayak.wav", (60.0, 63.0), 5000),
]

def prep_event(rel, a, b, lp):
    p = rel if os.path.isabs(rel) else src(rel)
    x = L.cut(L.load(p), a, b)
    x = L.norm_lufs(x, -20)
    x = L.leveler(x, 0.3, 8.0)      # 短電平器：削掉 1 秒內的爆點
    x = L.leveler(x, 0.1, 10.0)     # 更短一道：把提示音、門鈴的起音壓平
    x = tame(x, -28.0, 5.0)          # 快速壓縮：腳步、方向燈的瞬間峰值
    x = L.lowpass(x, lp)
    x = L.fade(x, 0.15, 0.5)
    x = L.reverb(x, mix=0.35, **RV)  # 事件先預濕一點（同組參數），起音更軟
    return L.norm_lufs(x, -20)

def build_events():
    bus = L.timeline(D)
    t = float(rng.uniform(1.0, 3.0))
    last = -1
    cache = {}
    while t < D - 0.5:
        k = int(rng.integers(len(EVENTS)))
        while k == last:
            k = int(rng.integers(len(EVENTS)))
        last = k
        name, rel, (a, b), lp = EVENTS[k]
        if k not in cache:
            cache[k] = prep_event(rel, a, b, lp)
        seg = cache[k]
        pan = float(rng.uniform(-0.5, 0.5))
        place_wrap(bus, seg, t, -5.0, pan)
        cues["events"].append(dict(t=round(t, 1), name=name, file=rel if not os.path.isabs(rel) else os.path.relpath(rel, R),
                                   cut=f"{a}–{b} s", dur_s=round(len(seg) / SR, 2), proc=f"norm −20、leveler 0.3 s/8 dB 再 0.1 s/10 dB、快速壓縮 −28 dB/5:1、低通 {lp} Hz、淡入 150 ms／淡出 500 ms、預濕殘響 mix 0.35", gain_db=-5, pan=round(pan, 2)))
        t += float(rng.uniform(5.0, 7.0)) + float(rng.uniform(-1.5, 1.5))
    return bus

# ------------------------------------------------------------------ 4. 身體與記憶層
READERS = ["小軒朗讀.wav", "柏成朗讀.wav", "阿瑤朗讀.wav"]

def build_body():
    bus = L.timeline(D + XF)
    br = L.load(os.path.join(R, "背景pad_20260908/素材/呼吸層_平靜版_240s_loop.wav"))
    br = L.norm_lufs(L.cut(br, 0, D + XF), -20)
    br = L.leveler(br, 3.0, 8.0)
    br = L.norm_lufs(L.lowpass(br, 5000), -20)
    L.place(bus, br, 0, -12.0, 0.0)
    cues["body"].append(dict(file="背景pad_20260908/素材/呼吸層_平靜版_240s_loop.wav", cut=f"0–{D + XF:.0f} s", proc="norm −20、leveler 3 s/8 dB、低通 5 kHz", gain_db=-12))
    bus = fold(bus)
    # 朗讀單詞：每 20 到 40 秒一個，三位朗讀者輪流
    words = {}
    for f in READERS:
        y = L.load(os.path.join(R, f))
        ph = [(a, b) for a, b in L.phrases(L.mono(y), top_db=30) if 0.6 <= b - a <= 2.6]
        words[f] = (y, ph)
    t = float(rng.uniform(6, 14))
    i = 0
    while t < D - 3:
        f = READERS[i % 3]
        y, ph = words[f]
        a, b = ph[int(rng.integers(len(ph)))]
        w = L.norm_lufs(L.cut(y, a, b), -20)
        w = L.lowpass(w, 3000)
        w = L.leveler(w, 0.2, 8.0)      # 壓平音節起音
        w = tame(w, -28.0, 5.0)
        w = L.fade(w, 0.12, 0.3)
        w = L.reverb(w, mix=0.55, **RV)     # 先預濕，再跟全體一起進同一組殘響
        w = L.norm_lufs(w, -20)
        pan = float(rng.uniform(-0.3, 0.3))
        place_wrap(bus, w, t, -4.0, pan)
        cues["memory"].append(dict(t=round(t, 1), name="朗讀單詞", file=f, cut=f"{a:.2f}–{b:.2f} s", proc="norm −20、低通 3 kHz、leveler 0.2 s/8 dB、快速壓縮 −28 dB/5:1、預濕殘響 mix 0.55（同組參數）、淡入 120 ms／淡出 300 ms", gain_db=-4, pan=round(pan, 2)))
        t += float(rng.uniform(20, 40)); i += 1
    # 小星星殘影：只用一次、5 秒以內
    tw = L.load(os.path.join(R, "效果測試_20260902/00_素材切段/小星星_第一句_0.52-19.90s_原始.wav"))
    tw = L.norm_lufs(L.cut(tw, 0.0, 4.5), -20)
    tw = L.reverse(L.lowpass(tw, 1200))
    tw = L.fade(tw, 1.5, 1.5)
    tw = L.norm_lufs(L.reverb(tw, mix=0.6, **RV), -20)
    t_tw = 97.0
    place_wrap(bus, tw, t_tw, -9.0, 0.0)
    cues["memory"].append(dict(t=t_tw, name="小星星殘影（一次）", file="效果測試_20260902/00_素材切段/小星星_第一句_0.52-19.90s_原始.wav", cut="0.0–4.5 s", proc="低通 1.2 kHz、反轉、淡入淡出各 1.5 s、預濕殘響 mix 0.6", gain_db=-9, pan=0.0))
    return bus

# ------------------------------------------------------------------ 量測輔助
def seam_check(y, w=1.0):
    """尾→頭接縫：最後 w 秒 與 最前 w 秒 的 RMS 差，以及跨接縫 10 秒視窗 vs 整段 LUFS。"""
    n = int(w * SR)
    tail, head = L.rms_db(y[-n:]), L.rms_db(y[:n])
    cross = np.concatenate([y[-5 * SR:], y[:5 * SR]])
    return dict(tail_rms_db=round(tail, 2), head_rms_db=round(head, 2), diff_db=round(abs(tail - head), 2),
                cross_10s_lufs=round(L.lufs(cross), 2), I_lufs=round(L.lufs(y), 2))

def window_lufs(y, win=10.0, hop=5.0):
    vals = []
    t = 0.0
    while t + win <= len(y) / SR + 1e-6:
        vals.append((round(t, 1), round(L.lufs(y[int(t * SR):int((t + win) * SR)]), 2)))
        t += hop
    v = np.array([b for _, b in vals])
    return dict(n=len(vals), min=float(v.min()), max=float(v.max()), spread=float(v.max() - v.min()),
                argmin_t=vals[int(v.argmin())][0], argmax_t=vals[int(v.argmax())][0])

def rms_jump(y, win=0.05, skip=1.0):
    m = L.mono(y)
    h = int(win * SR)
    n = len(m) // h
    e = np.array([L.rms_db(m[i * h:(i + 1) * h]) for i in range(n)])
    k = int(skip / win)
    d = np.abs(np.diff(e))[k:len(e) - k]
    return dict(max_jump_db=float(d.max()), at_s=float((int(d.argmax()) + k) * win))

# ------------------------------------------------------------------ 主流程
def main():
    floor = build_floor()
    transport = build_transport()
    events = build_events()
    body = build_body()
    mix = floor + transport + events + body
    # 共用殘響：線性，所以尾巴繞回開頭等於循環卷積，接縫依然連續
    wet = L.reverb(mix, mix=RV_MIX, **RV)
    dry_len = len(mix)
    y = wet[:dry_len].copy()
    tail = wet[dry_len:]
    y[:len(tail)] += tail
    y = L.lowpass(y, 7500)
    y = L.highpass(y, 60)
    y = y - (1 - L.db(-5.0)) * L.lowpass(y, 250, 1)   # 低架 −5 dB（250 Hz 以下），把重心往參考檔的 700 Hz 到 2 kHz 拉
    y = L.finalize(y, edge_fade_s=0.0)
    seam = seam_check(y)
    y = L.fade(y, 1.0, 1.0)      # lib 規定的頭尾 1 秒短淡化
    out = os.path.join(OUT_DIR, f"B_{TITLE}_{int(D)}s.wav")
    L.write(out, y)
    rep = L.measure(out)
    ok = L.check(rep)
    win = window_lufs(y)
    jump = rms_jump(y)
    spec = L.spectral_summary(y)
    result = dict(out=out, measure=rep, check=bool(ok), seam=seam, window10s=win, rms_jump50ms=jump, spectrum=spec,
                  duration_s=len(y) / SR, seed=SEED, reverb=dict(RV, mix=RV_MIX), cues=cues)
    with open(os.path.join(HERE, "B_cues.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    os.makedirs(os.path.join(OUT_DIR, "scripts"), exist_ok=True)
    shutil.copy(os.path.abspath(__file__), os.path.join(OUT_DIR, "scripts", "B_build.py"))
    print(json.dumps({k: v for k, v in result.items() if k != "cues"}, ensure_ascii=False, indent=1))
    print("CHECK", "OK" if ok else "FAIL")

if __name__ == "__main__":
    main()
