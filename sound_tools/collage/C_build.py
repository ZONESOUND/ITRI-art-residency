# -*- coding: utf-8 -*-
"""
C_build.py：《節奏繞纏》第四幕旅行拼貼，代號 C「記憶碎片」。
Schaeffer 式聲音物件手勢拼貼：從旅行素材切 0.3 到 3 秒的碎片，短交叉淡化串成句子，
句子之間長交叉淡化；三支慢速一個八度的低通素材交錯 loop 成連續低頻地板；
動機碎片（安全帶提示音、地鐵門 beep、遠方汽笛、方向燈）每 12 到 20 秒回來一次並變形。

重跑：
    cd <scratchpad> && source .venv/bin/activate && python agent_C/C_build.py
"""
import os, sys, math, json, shutil
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import collage_lib as L

SR = L.SR
T = L.TRAVEL
OUT_DIR = os.path.join(T, "拼貼試做_20260915")
CODE = "C"
TITLE = "記憶碎片"
TARGET = -20.0

# 共用空間（整支檔只用這一組）
RV = dict(rt60=2.6, lp_hz=4000, predelay_ms=20, mix=0.33)
DL = dict(time_s=0.375, fb=0.35, lp_hz=3000, mix=0.18)
GLOBAL_LP = 7000
FLOOR_DB = -7.0   # 地板相對主層

# ------------------------------------------------------------------ 來源表
SRC_PATHS = {
    # 空中
    "seatbelt_dry": "01_飛機與機場/FF_MT_airplane_foley_seatbelt_sign_dry.wav",
    "seatbelts_act": "01_飛機與機場/BRS_Activity_Plane_Seatbelts1.wav",
    "turb": "01_飛機與機場/BRS_Plane_Turbulance_Hard_1.wav",
    "lug_heavy": "01_飛機與機場/BRS_Wheels_Luggage_Bag_OB_Roll_Heavy_1.wav",
    "lug_med": "01_飛機與機場/BRS_Wheels_Luggage_Bag_OB_Roll_Med.wav",
    "fall": "01_飛機與機場/FF_MT_airplane_foley_fall.wav",
    "runway": "01_飛機與機場/FF_MT_airplane_foley_runway_riser.wav",
    "fa39": "01_飛機與機場/FlightAttendant_S08TA.39.wav",
    "jet": "01_飛機與機場/JetKc135PassBy_SFXB.4295.wav",
    "tokyo": "01_飛機與機場/PSE_GGV1_FX_One_Shot_Ambience_Tokyo_Airport_Departure_Lobby.wav",
    "deepwind": "06_風與空氣/FF_IE_fx_deep_wind.wav",
    "kshmr": "06_風與空氣/KSHMR_Ambiance_-_Airy_10__G_.wav",
    "glacier": "06_風與空氣/FF_SFXT_foley_glacier_wind_tonal.wav",
    # 軌道（算地面）
    "tube_doors": "02_火車與地鐵/FF_MT_london_underground_foley_doors_open_low_beep.wav",
    "horn_std": "02_火車與地鐵/FF_MT_train_foley_horn_standard.wav",
    "hornblow": "02_火車與地鐵/TrainHornBlow_BWU11.286.wav",
    "horndist": "02_火車與地鐵/TrainHornDist_SEU04.48.wav",
    "bart_c": "02_火車與地鐵/Subway_Bart__Train_Interior_Station_Doors_Crowded_05.wav",
    "bart_q": "02_火車與地鐵/Subway_Bart__Train_Interior_Station_Doors_Quiet_04.wav",
    "amtrak17": "02_火車與地鐵/TrainAmtrak_S08TT.17.wav",
    "trainpass": os.path.join(L.ROOT, "其他音效素材/FF_EFX_ambience_train_passing_fast.wav"),
    # 地面
    "turnsig": "03_道路與城市/CarTurnSignal_BW.62374.wav",
    "trfdc": "03_道路與城市/TRFDC_Cuts_Travel_08.wav",
    "bus": "03_道路與城市/FF_CL_ambience_london_bus_station_red.wav",
    "road": "03_道路與城市/Road_01.wav",
    "kayak": "04_水上與船/FF_MC_foley_paddling_sea_kayak.wav",
    "paddleboat": "04_水上與船/PaddleBoat_BW.60746.wav",
    "pontoon": "04_水上與船/PontoonBoatMedium_BW.5320.M.wav",
    "pirate": "04_水上與船/PirateShipOceanWaves_SFXB.1.wav",
    "walk": "05_自行車與步行/ASO_foley_walking_outside.wav",
    "pedals": "05_自行車與步行/Bike_Pedals.wav",
    "wheelspin": "05_自行車與步行/ESM_Explainer_Video_One_Shot_Foley_Bike_Wheel_Spin_Bicycle_Street_6.wav",
    "fs_gravel": os.path.join(L.ROOT, "腳步聲素材/FootstepsGravel_BW.7744.wav"),
    "fs_leaves": os.path.join(L.ROOT, "腳步聲素材/FootstepsLeaves_BW.7917.wav"),
    "fs_cement": os.path.join(L.ROOT, "腳步聲素材/FootstepsCement_BW.7554.wav"),
    "fs_juming": os.path.join(L.ROOT, "腳步聲素材/2022朱銘美術館_腳步.wav"),
    "fs_bike_leaves": os.path.join(L.ROOT, "腳步聲素材/2024聲響單車_LeavesFootsteps.wav"),
    # 朗讀與小星星
    "read_xuan": os.path.join(L.ROOT, "小軒朗讀.wav"),
    "read_bocheng": os.path.join(L.ROOT, "柏成朗讀.wav"),
    "read_ayao": os.path.join(L.ROOT, "阿瑤朗讀.wav"),
    "twinkle": os.path.join(L.ROOT, "效果測試_20260902/00_素材切段/小星星_第一句_0.52-19.90s_原始.wav"),
}
_SRC = {}
def src(k):
    if k not in _SRC:
        p = SRC_PATHS[k]
        _SRC[k] = L.load(p if os.path.isabs(p) else os.path.join(T, p))
    return _SRC[k]

# ------------------------------------------------------------------ 碎片表（名稱：來源、起點秒、長度秒、組別、各自低通）
# 組別：G 地面（腳步、單車、路、水上、軌道）、A 空中（機場、飛機、風）、W 朗讀單詞、S 小星星、M 動機
FR = {
    # 動機
    "belt":      ("seatbelt_dry", 0.95, 1.30, "M", 5000),   # 安全帶提示音
    "beep":      ("tube_doors", 0.75, 1.40, "M", 5000),     # 地鐵門 beep
    "horn_far":  ("horndist", 0.20, 1.80, "M", 4000),       # 遠方汽笛
    "blink":     ("turnsig", 0.55, 0.75, "M", 6000),        # 方向燈兩格
    # 空中
    "belt_click": ("seatbelts_act", 8.25, 0.55, "A", None),
    "turb_bump": ("turb", 19.55, 1.60, "A", 4000),
    "lug_h":     ("lug_heavy", 1.00, 2.60, "A", 4500),
    "lug_m":     ("lug_med", 2.00, 2.00, "A", 4500),
    "whoosh":    ("fall", 3.00, 1.60, "A", 4000),
    "runway_end": ("runway", 23.9, 2.00, "A", 4000),        # 跑道加速的最後兩秒
    "pa":        ("fa39", 0.35, 0.80, "A", 4500),           # 機艙廣播碎片
    "doppler":   ("jet", 5.30, 3.00, "A", 4500),            # 噴射機掠過的都卜勒中段
    "lobby":     ("tokyo", 14.20, 2.60, "A", 5000),
    "lobby2":    ("tokyo", 20.60, 1.80, "A", 5000),
    "dwind":     ("deepwind", 0.20, 2.00, "A", 4000),
    "airy":      ("kshmr", 0.30, 2.00, "A", 5000),
    "glacier":   ("glacier", 5.00, 3.00, "A", 4000),
    # 軌道
    "horn_head": ("horn_std", 0.00, 1.20, "G", 4000),       # 汽笛的頭
    "hornblow":  ("hornblow", 0.25, 1.10, "G", 4000),
    "door_c":    ("bart_c", 3.00, 1.50, "G", 5000),         # 門開的那一下
    "door_q":    ("bart_q", 6.30, 1.50, "G", 5000),
    "amtrak":    ("amtrak17", 1.85, 1.20, "G", 4000),
    "trainpass": ("trainpass", 4.60, 2.60, "G", 3500),
    # 地面
    "cut08":     ("trfdc", 0.00, 1.90, "G", 5000),
    "bus":       ("bus", 2.00, 2.40, "G", 4500),
    "paddle1":   ("kayak", 17.85, 1.20, "G", 5000),         # 划槳一下
    "paddle2":   ("kayak", 40.95, 1.30, "G", 5000),
    "pboat":     ("paddleboat", 5.00, 2.60, "G", 4000),
    "pontoon":   ("pontoon", 3.00, 2.20, "G", 4500),
    "walk_a":    ("walk", 2.00, 1.40, "G", 5000),
    "walk_b":    ("walk", 22.85, 1.00, "G", 5000),
    "pedal":     ("pedals", 3.00, 1.50, "G", 5000),
    "spin":      ("wheelspin", 2.00, 2.60, "G", 5000),
    "step_grav": ("fs_gravel", 0.50, 0.55, "G", 5000),      # 腳步一步
    "step_grav2": ("fs_gravel", 1.50, 1.05, "G", 5000),     # 兩步
    "step_leaf": ("fs_leaves", 1.85, 0.55, "G", 5000),
    "step_leaf2": ("fs_leaves", 2.90, 1.05, "G", 5000),
    "step_cem":  ("fs_cement", 1.95, 0.80, "G", 5000),
    "step_jm":   ("fs_juming", 1.45, 0.65, "G", 5000),
    "step_jm2":  ("fs_juming", 3.15, 0.90, "G", 5000),
    "bikeleaf":  ("fs_bike_leaves", 10.0, 1.60, "G", 5000),
    # 朗讀單詞（用 L.phrases 切出的區段；不宣稱是哪個字）
    "w_x1": ("read_xuan", 6.13, 0.85, "W", 6000),
    "w_x2": ("read_xuan", 13.86, 1.01, "W", 6000),
    "w_x3": ("read_xuan", 27.37, 0.79, "W", 6000),
    "w_x4": ("read_xuan", 39.78, 1.10, "W", 6000),
    "w_b1": ("read_bocheng", 7.95, 0.78, "W", 6000),
    "w_b2": ("read_bocheng", 11.86, 0.59, "W", 6000),
    "w_b3": ("read_bocheng", 19.79, 0.58, "W", 6000),
    "w_b4": ("read_bocheng", 38.16, 0.83, "W", 6000),
    "w_a1": ("read_ayao", 48.04, 0.85, "W", 6000),
    "w_a2": ("read_ayao", 51.00, 0.97, "W", 6000),
    "w_a3": ("read_ayao", 66.68, 1.28, "W", 6000),
    "w_a4": ("read_ayao", 77.56, 1.11, "W", 6000),
    # 小星星第一句（只准這一句）
    "tw1": ("twinkle", 0.00, 1.10, "S", 1200),
    "tw2": ("twinkle", 2.45, 1.20, "S", 1200),
    "tw3": ("twinkle", 4.90, 1.00, "S", 1200),
    "tw4": ("twinkle", 9.80, 1.30, "S", 1200),
    "tw5": ("twinkle", 14.70, 1.20, "S", 1200),
}

# ------------------------------------------------------------------ 碎片處理
def norm_short(x, target=TARGET):
    """短碎片的響度正規化：不到 1 秒的先平鋪到 1.5 秒再量，避免 pyloudnorm 對短檔失效。"""
    x = L.stereo(x)
    if len(x) < int(1.5 * SR):
        reps = int(math.ceil(1.5 * SR / len(x)))
        ref = np.concatenate([x] * reps)
    else:
        ref = x
    cur = L.lufs(ref)
    if cur <= -69:
        return x
    return x * L.db(target - cur)

def frag(name, semi=0, rev=False, gain=0.0, lp=None):
    """切碎片：低通 → 變速 → 反轉 → 響度拉平 → 頭尾等功率淡化。"""
    fkey, st, du, grp, lp0 = FR[name]
    x = L.cut(src(fkey), st, dur_s=du)
    if name == "blink":
        # 方向燈兩格之間是近乎全靜音，單獨放會變硬切：墊一段路面聲當底床（−10 dB），像在車裡聽到
        bed = L.lowpass(L.cut(src("road"), 5.0, dur_s=du), 2000)
        x = L.norm_lufs(x, TARGET) + L.norm_lufs(bed, TARGET) * L.db(-10)
    lp_hz = lp if lp is not None else lp0
    if lp_hz:
        x = L.lowpass(x, lp_hz)
    if semi:
        x = L.varispeed(x, semi)
    if rev:
        x = L.reverse(x)
    x = L.leveler(x, 0.10, 16)          # 短電平器：把碎片內的瞬態（腳步、撞擊）壓平，避免 50 ms 尺度硬切
    x = norm_short(x) * L.db(gain)
    n = len(x) / SR
    x = L.fade(x, max(0.06, 0.15 * n), max(0.08, 0.25 * n))
    return x

# ------------------------------------------------------------------ 句子表
# 每個元素：(碎片名, 半音, 反轉, 增益 dB)；xf 是句內交叉淡化秒數（0.15 到 0.6）
def f(name, semi=0, rev=False, gain=0.0):
    return (name, semi, rev, gain)

SENTENCES = [
    # 1 地面：出門
    dict(xf=0.3, items=[f("step_grav"), f("step_grav2"), f("blink"), f("walk_a"), f("step_cem"), f("w_x1"), f("spin"), f("belt"), f("bus", 0, False, -1)]),
    # 2 地面偏軌道：月台
    dict(xf=0.35, items=[f("pedal"), f("beep"), f("door_q"), f("step_leaf"), f("w_b1", -3), f("amtrak"), f("horn_far"), f("pboat"), f("bikeleaf"), f("cut08")]),
    # 3 空中初現：登機口
    dict(xf=0.4, items=[f("lug_m"), f("belt", 5), f("lobby"), f("belt_click"), f("w_a1"), f("step_jm"), f("pa", 0, True), f("lug_h"), f("blink", 0, True), f("airy")]),
    # 4 倒回地面：水上
    dict(xf=0.3, items=[f("paddle1"), f("paddle2"), f("beep", -7), f("pontoon"), f("step_leaf2"), f("w_x2", 0, True), f("hornblow"), f("horn_far", 0, True), f("trainpass")]),
    # 5 空中：起飛
    dict(xf=0.45, items=[f("runway_end"), f("belt", -7), f("whoosh"), f("turb_bump"), f("w_b2"), f("blink", -5), f("dwind"), f("doppler"), f("lobby2", 0, True)]),
    # 6 空中：巡航
    dict(xf=0.5, items=[f("glacier"), f("beep", 5), f("lug_h", 0, True), f("w_a2", -3), f("airy", -5), f("horn_far", -5), f("belt_click", -7), f("pa"), f("dwind", 0, True)]),
    # 7 倒回地面：記起腳步
    dict(xf=0.25, items=[f("step_jm2"), f("step_grav"), f("blink"), f("walk_b"), f("door_c"), f("w_x3"), f("step_leaf"), f("beep", 0, True), f("pedal", -5), f("bus", -5, False, -1)]),
    # 8 混合：車站與艙門
    dict(xf=0.4, items=[f("amtrak", 0, True), f("belt", 0, True), f("spin", -5), f("lug_m", 0, True), f("w_b3"), f("horn_far", 5), f("turb_bump", -5), f("trainpass", 0, True)]),
    # 9 空中：風與都卜勒
    dict(xf=0.5, items=[f("doppler", -5), f("beep", -7, True), f("glacier", 0, True), f("w_a3"), f("blink", 5), f("whoosh", 0, True), f("dwind"), f("belt", 5, True)]),
    # 10 空中：機場大廳回音
    dict(xf=0.45, items=[f("lobby2"), f("lug_h", -5), f("belt_click", 5), f("w_b4", -3), f("pa", -5), f("horn_far", 0, True), f("airy", 0, True), f("runway_end", -5)]),
    # 11 倒回地面：水面與單車
    dict(xf=0.3, items=[f("pboat", -3), f("paddle2", 0, True), f("blink", -7), f("bikeleaf", -3), f("w_a4"), f("door_c", 0, True), f("beep"), f("pedal", 0, True), f("cut08", -5)]),
    # 12 混合：門與亂流
    dict(xf=0.4, items=[f("door_q"), f("turb_bump", 5), f("belt", -7), f("step_cem"), f("w_x4"), f("hornblow", 0, True), f("whoosh", -5), f("lobby", 0, True), f("horn_far", -7)]),
    # 13 後三分之一起：小星星殘影開始
    dict(xf=0.45, items=[f("tw1", -12), f("lobby"), f("horn_far", 0, True), f("step_cem", -3), f("w_x4", -3), f("lug_h"), f("beep"), f("airy", 0, True)]),
    # 14 地面最後一次回頭
    dict(xf=0.3, items=[f("step_grav2", -3), f("paddle1", -3), f("blink", -7), f("tw2", -12), f("w_b4"), f("door_q", 0, True), f("hornblow", -5), f("pboat", -5), f("belt", -7, True)]),
    # 15 空中：飛遠
    dict(xf=0.5, items=[f("doppler", 0, True), f("tw3", -12), f("beep", 5, True), f("turb_bump"), f("w_a4", -3), f("horn_far", -7), f("glacier", -5), f("runway_end", 0, True)]),
    # 16 空中：只剩風和提示音
    dict(xf=0.55, items=[f("dwind", -5), f("belt"), f("tw4", -12), f("airy"), f("w_x1", 0, True), f("blink", 0, True), f("whoosh", -5), f("belt_click", 0, True)]),
    # 17 空中：都卜勒與行李輪最後一次
    dict(xf=0.5, items=[f("doppler", -7), f("lug_m", -5), f("beep", -7), f("glacier", -5), f("w_b2", 0, True), f("horn_far", 5), f("trainpass", -5, True), f("lobby2", -5)]),
    # 18 尾：最後一顆星、最後一個提示音
    dict(xf=0.6, items=[f("glacier", -5, True), f("tw5", -12), f("beep", -7), f("lug_m", -5), f("w_a1", 0, True), f("belt", 5), f("dwind", 0, True), f("doppler", -7)]),
]
SENT_XF = [2.5, 3.0, 2.5, 3.0, 3.5, 2.5, 3.0, 3.0, 3.5, 3.0, 2.5, 3.0, 3.5, 3.0, 3.5, 3.0, 4.0]  # 句與句之間

# ------------------------------------------------------------------ 組句
def build_sentence(spec):
    segs, meta = [], []
    for name, semi, rev, gain in spec["items"]:
        x = frag(name, semi, rev, gain)
        segs.append(x)
        meta.append(dict(name=name, semi=semi, rev=rev, gain=gain, dur=len(x) / SR))
    xf = spec["xf"]
    # 交叉淡化不能長於相鄰碎片的一半
    xfs = [min(xf, len(a) / SR * 0.5, len(b) / SR * 0.5) for a, b in zip(segs[:-1], segs[1:])]
    y = L.xfade_concat(segs, xfs)
    # 句內偏移
    t = 0.0
    for k, m in enumerate(meta):
        m["off"] = t
        if k < len(xfs):
            t += m["dur"] - xfs[k]
    y = L.norm_lufs(y, TARGET)
    return y, meta

def build_floor(dur):
    """低頻地板：三支慢一個八度、低通 400 Hz、交錯 loop。"""
    parts = []
    for key, st, du, seed_off in [("jet", 1.0, 18.0, 0), ("pirate", 20.0, 40.0, 7), ("turb", 0.5, 22.0, 13)]:
        x = L.cut(src(key), st, dur_s=du)
        x = L.varispeed(x, -12)
        x = L.lowpass(x, 400, 2)
        x = L.highpass(x, 55, 2)
        x = L.norm_lufs(x, TARGET)
        x = L.fade(x, 2.0, 2.0)
        parts.append(x)
    bus = L.timeline(dur + 10)
    t = 0.0; k = 0
    # 三支輪流放，每段長度略有不同，重疊 4 秒
    while t < dur + 5:
        x = parts[k % 3]
        seg_len = min(len(x) / SR, 14 + 5 * ((k * 7) % 3))
        seg = L.fade(x[:int(seg_len * SR)], 3.0, 3.0)
        L.place(bus, seg, t, 0.0, 0.0)
        t += seg_len - 4.0
        k += 1
    bus = bus[:int(dur * SR)]
    bus = L.leveler(bus, 2.0, 10)
    return L.norm_lufs(bus, TARGET)

def jump_check(x, win_s=0.05, edge_s=1.0):
    m = L.mono(x); w = int(win_s * SR); n = len(m) // w
    r = 20 * np.log10(np.sqrt(np.mean(m[:n * w].reshape(n, w) ** 2, axis=1)) + 1e-9)
    e = int(edge_s / win_s)
    r = r[e:-e]
    d = np.abs(np.diff(r))
    i = int(np.argmax(d))
    return float(d.max()), (i + e) * win_s, d

# ------------------------------------------------------------------ 主流程
def main():
    sent_audio, sent_meta = [], []
    for k, spec in enumerate(SENTENCES):
        y, meta = build_sentence(spec)
        sent_audio.append(y); sent_meta.append(meta)
        print(f"句 {k+1:2d}: {len(y)/SR:5.1f} s, {len(meta)} 碎片, LUFS {L.lufs(y):.1f}")
    xfs = [min(x, len(a) / SR * 0.45, len(b) / SR * 0.45) for x, a, b in zip(SENT_XF, sent_audio[:-1], sent_audio[1:])]
    main_chain = L.xfade_concat(sent_audio, xfs)
    # 句子起點
    starts = [0.0]
    for k in range(len(sent_audio) - 1):
        starts.append(starts[-1] + len(sent_audio[k]) / SR - xfs[k])
    dur = len(main_chain) / SR
    print("主鏈長度", round(dur, 1))

    # 短期響度先自己拉平（0.5 s 細電平器），再整體同一組殘響與同步 delay
    main_chain = L.leveler(main_chain, 0.5, 6)
    main_chain = L._compress(main_chain, thresh_db=-26, ratio=3.0, attack_s=0.003, release_s=0.12)  # 快速壓縮：抓 50 ms 尺度的殘餘瞬態
    main_chain = L.highpass(main_chain, 120, 2)
    main_chain = L.norm_lufs(main_chain, TARGET)
    wet = L.reverb(main_chain, **RV)
    wet = L.delay(wet, **DL)

    floor = build_floor(dur)
    floor = L.reverb(floor, **RV)

    total = max(len(wet), len(floor))
    tl = L.timeline(total / SR)
    L.place(tl, wet, 0.0, 0.0)
    L.place(tl, floor, 0.0, FLOOR_DB)
    tl = tl[:int(dur * SR)]  # 尾巴截掉：finalize 的 1 秒淡出處理收尾
    tl = L.lowpass(tl, GLOBAL_LP, 2)
    tl = L.leveler(tl, 0.10, 12)        # 合成後的快速電平器：專門抓 50 ms 尺度的跳變（硬切檢查）
    out = L.finalize(tl, tp_db=-3.6)   # 樣本峰限幅 −3.6，留 0.6 dB 給真峰值

    sec = int(round(len(out) / SR))
    base = f"{CODE}_{TITLE}_{sec}s"
    wav = os.path.join(OUT_DIR, base + ".wav")
    L.write(wav, out)
    rep = L.measure(wav)
    ok = L.check(rep)
    jmax, jt, _ = jump_check(out)
    spec = L.spectral_summary(out)
    print("measure", rep, "check", ok)
    print(f"最大 50 ms RMS 跳變 {jmax:.2f} dB @ {jt:.2f} s")
    print("spectral", spec)

    # 統計
    n_frag = sum(len(m) for m in sent_meta)
    files_used = set(FR[m["name"]][0] for meta in sent_meta for m in meta) | {"jet", "pirate", "turb"}
    motif_counts = {k: 0 for k in ["belt", "beep", "horn_far", "blink"]}
    motif_times = {k: [] for k in motif_counts}
    tw_count = 0
    for s, meta in zip(starts, sent_meta):
        for m in meta:
            if m["name"] in motif_counts:
                motif_counts[m["name"]] += 1
                motif_times[m["name"]].append(round(s + m["off"], 1))
            if FR[m["name"]][3] == "S":
                tw_count += 1
    stats = dict(n_frag=n_frag, n_files=len(files_used), motif_counts=motif_counts, motif_times=motif_times,
                 twinkle=tw_count, starts=[round(s, 1) for s in starts], dur=round(len(out) / SR, 1))
    json.dump(dict(measure=rep, check=ok, jump_max_db=jmax, jump_at_s=jt, spectral=spec, stats=stats,
                   sentences=sent_meta), open(os.path.join(HERE, "C_result.json"), "w"), ensure_ascii=False, indent=1)

    write_md(os.path.join(OUT_DIR, f"{CODE}_{TITLE}_設計說明.md"), base, rep, ok, jmax, jt, spec, stats, starts, sent_meta)
    os.makedirs(os.path.join(OUT_DIR, "scripts"), exist_ok=True)
    shutil.copy(os.path.abspath(__file__), os.path.join(OUT_DIR, "scripts", "C_build.py"))
    return wav, rep, ok

# ------------------------------------------------------------------ 設計說明
GROUP_NAME = {"G": "地面", "A": "空中", "W": "朗讀", "S": "小星星", "M": "動機"}
SENT_TITLE = ["出門：腳步與方向燈", "月台：門與遠笛", "登機口：行李輪與提示音", "倒回地面：划槳與水面",
              "起飛：跑道尾端與都卜勒", "巡航：冰河風與艙內", "倒回地面：記起腳步", "車站與艙門混在一起",
              "風與都卜勒", "機場大廳回音", "倒回地面：水面與單車", "門與亂流", "小星星殘影開始",
              "地面最後一次回頭", "飛遠", "只剩風和提示音", "都卜勒與行李輪最後一次", "最後一顆星"]

def fname(key):
    return os.path.basename(SRC_PATHS[key])

def write_md(path, base, rep, ok, jmax, jt, spec, stats, starts, sent_meta):
    o = []
    o.append(f"# {CODE}《{TITLE}》設計說明\n")
    o.append(f"輸出：`{base}.wav`（同名 `.mp3`），長度 {stats['dur']} 秒，48 kHz、24-bit 立體聲。\n")
    o.append("## 一、剪輯邏輯與聽感設計\n")
    o.append("這一版把素材當「聲音物件」而不是「場景」：從 44 支旅行素材與腳步、朗讀、小星星裡切出 0.3 到 3 秒的碎片"
             "（門開的那一下、安全帶提示音、汽笛的頭、划槳一下、方向燈兩格、腳步一步、行李輪一段、噴射機掠過的都卜勒中段、"
             "跑道加速的最後兩秒），每個碎片先各自拉到 −20 LUFS、頭尾等功率淡化，再用 0.15 到 0.6 秒的短交叉淡化串成十八個「句子」，"
             "句子之間用 2.5 到 4 秒的交叉淡化接起來。聽感上像一個人在翻旅行的記憶：碎片會回來，回來時變速或反轉。"
             "全程底下有一條連續的低頻地板（噴射機、海浪、亂流三支各慢一個八度、低通 400 Hz、交錯循環，相對主層 −7 dB），"
             "那是「飛翔」的身體感，也保證任何時刻都不會空掉。碎片來源在「地面」與「空中」兩組之間逐句換比例：開頭多地面，"
             "後段多空中，但第四句、第七句、第十一句、第十四句各倒回地面一次，不是線性往上。四個動機（安全帶提示音、地鐵門 beep、"
             "遠方汽笛、方向燈兩格）每 12 到 20 秒輪流回來，每次略變（原速、+5、−5、−7 半音、反轉）。朗讀單詞每句最多一個，"
             "與其他碎片同響度、同殘響，偶爾反轉或慢 3 個半音，不做成旁白。小星星只用第一句，切成 1 到 1.3 秒的碎片、慢一個八度、"
             "低通 1.2 kHz，散在後三分之一，共五次。質地統一靠三件事：所有碎片同一響度、整支主鏈過同一組殘響"
             f"（rt60 {RV['rt60']} s、低通 {RV['lp_hz']} Hz、mix {RV['mix']}）和同一條同步 delay（{DL['time_s']} s、fb {DL['fb']}、mix {DL['mix']}）"
             f"讓碎片有共同的尾巴並填掉空隙，整體再低通 {GLOBAL_LP} Hz 收斂高頻，最後 `finalize` 收尾。\n")
    o.append("## 二、時間軸 cue 表（以句子為單位）\n")
    o.append("秒數為句子起點（與前一句有交叉淡化重疊）；碎片依序列出，格式：來源檔名 [起點秒 + 長度秒] 處理。層別：主層＝碎片鏈；地板＝低頻持續層。\n")
    for k, (s, meta) in enumerate(zip(starts, sent_meta)):
        gcount = {}
        for m in meta:
            g = FR[m["name"]][3]; gcount[g] = gcount.get(g, 0) + 1
        gtxt = "、".join(f"{GROUP_NAME[g]} {n}" for g, n in gcount.items())
        o.append(f"### 句 {k+1}（{s:.1f} s 起）：{SENT_TITLE[k]}　［{gtxt}］\n")
        for m in meta:
            key, st, du, grp, lp0 = FR[m["name"]]
            proc = []
            if lp0: proc.append(f"低通 {lp0} Hz")
            if m["semi"]: proc.append(f"變速 {m['semi']:+d} 半音")
            if m["rev"]: proc.append("反轉")
            if m["gain"]: proc.append(f"增益 {m['gain']:+.0f} dB")
            proc.append("pan 0")
            o.append(f"- {s + m['off']:.1f} s：`{fname(key)}` [{st:.2f} + {du:.2f}]　{'／'.join(proc)}　（{GROUP_NAME[grp]}，主層）")
        o.append("")
    o.append("### 地板層（0 s 到結尾，連續）\n")
    o.append(f"- `{fname('jet')}` [1.00 + 18.00]、`{fname('pirate')}` [20.00 + 40.00]、`{fname('turb')}` [0.50 + 22.00]：各變速 −12 半音／低通 400 Hz／norm −20 LUFS，三支輪流、每段 14 到 24 秒、重疊 4 秒交叉淡化，整層再過 2 秒電平器，高通 55 Hz，相對主層 −7 dB，同一組殘響。\n")
    o.append("### 共用處理（整支）\n")
    o.append(f"- 方向燈兩格：兩格之間近乎全靜音，墊一段 `Road_01.wav` [5.00 + 0.75] 低通 2 kHz、−10 dB 當底床。\n- 每個碎片：0.10 秒短電平器（±16 dB）壓瞬態 → 響度拉平到 −20 LUFS → 頭尾等功率淡化。\n- 主鏈：0.5 秒細電平器（±6 dB）→ 快速壓縮（門檻 −26 dB、3:1、attack 3 ms、release 120 ms）→ 高通 120 Hz → 殘響 rt60 {RV['rt60']} s、lp {RV['lp_hz']} Hz、predelay {RV['predelay_ms']} ms、mix {RV['mix']} → delay {DL['time_s']} s、fb {DL['fb']}、lp {DL['lp_hz']} Hz、mix {DL['mix']}。\n"
             f"- 合成後：低通 {GLOBAL_LP} Hz → 0.10 秒快速電平器（±12 dB，專抓 50 ms 尺度跳變）→ `finalize`（3 s 與 1 s 電平器、軟壓縮、限幅（樣本峰 −3.6 dB）、正規化 −20 LUFS、頭尾 1 秒淡化）。\n")
    o.append("## 三、量測\n")
    o.append("```")
    o.append(json.dumps(rep, ensure_ascii=False))
    o.append(f"check() = {ok}")
    o.append(f"最大 50 ms 視窗 RMS 跳變（頭尾 1 秒除外）= {jmax:.2f} dB，位置 {jt:.2f} s")
    o.append(f"頻譜摘要 = {json.dumps(spec, ensure_ascii=False)}")
    o.append("```\n")
    mt = stats["motif_times"]
    o.append("統計：碎片 {} 個、來源檔 {} 支（含地板三支）。動機回來次數：安全帶提示音 {} 次（{}）、地鐵門 beep {} 次（{}）、遠方汽笛 {} 次（{}）、方向燈 {} 次（{}）。小星星碎片 {} 次。\n".format(
        stats["n_frag"], stats["n_files"],
        stats["motif_counts"]["belt"], "、".join(f"{t} s" for t in mt["belt"]),
        stats["motif_counts"]["beep"], "、".join(f"{t} s" for t in mt["beep"]),
        stats["motif_counts"]["horn_far"], "、".join(f"{t} s" for t in mt["horn_far"]),
        stats["motif_counts"]["blink"], "、".join(f"{t} s" for t in mt["blink"]),
        stats["twinkle"]))
    o.append("## 四、試聽時請注意\n")
    o.append("1. 任意點按下去：主鏈的碎片密度會變，但短期響度應該不變；請特別在句與句交接（cue 表各句起點前後 3 秒）試按。")
    o.append("2. 動機是否認得出來：安全帶提示音變速後（+5、−7 半音）還聽得出是同一個東西嗎？如果反轉版聽不出來，可以把反轉改成只變速。")
    o.append("3. 朗讀單詞是否跳出來：它們跟其他碎片同響度、同殘響；如果覺得人聲太前面，把 `W` 組碎片整體再減 3 dB。")
    o.append("4. 低頻地板夠不夠「飛」：三支慢一個八度的素材相對主層 −7 dB；在大喇叭上聽會比耳機明顯，太滿可退到 −10 dB。")
    o.append("5. 小星星殘影（後三分之一，五次）慢一個八度後只剩輪廓；聽得出是那首歌嗎？不必聽得出，但也不要變成一坨低頻。\n")
    o.append("## 五、弱點與下一步\n")
    o.append("- 碎片拼貼的本質是短事件密集，殘響與 delay 填空隙之後有些碎片的「頭」會被前一個碎片的尾巴糊掉，辨識度比場景式拼貼低；如果要更清楚，可以把句內交叉淡化縮到 0.15 到 0.25 秒，但要重跑硬切檢查。")
    o.append("- 電平器把每個碎片壓到同一平面，代價是原本強弱對比（門撞擊、汽笛）被抹平，聽起來比較像「一串等重的物件」；這是設計選擇，但可能少了戲劇性。")
    o.append("- 地面與空中的比例是手寫的句子表，沒有做真正的隨機化；每次重跑結果相同，適合定稿，不適合做多版本抽籤。")
    o.append("- 下一步：（1）請紀柏豪挑出他覺得最像「記憶」的三到四個碎片，把它們升格為主要動機、其餘動機減少；（2）試一版句內交叉淡化更短、殘響 mix 0.25 的清晰版比較；（3）如果要跟 A、B 兩版銜接，可共用同一組殘響參數。")
    open(path, "w", encoding="utf-8").write("\n".join(o))

if __name__ == "__main__":
    main()
