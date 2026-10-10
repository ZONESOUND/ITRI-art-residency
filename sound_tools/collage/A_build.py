"""
A_build.py：《節奏繞纏》第四幕旅行拼貼，代號 A「從腳步到天空」。
剪輯邏輯：單向線性成長旅程，尺度由小到大、由地面到空中：
  S1 步行與自行車 → S2 道路與城市 → S3 火車與地鐵 → S4 水上與船 → S5 機場與起飛 → S6 風與呼吸
每段各自 norm_lufs 到 −20 再串接（尺度變大靠頻譜與密度，不靠音量），段與段 7 到 9 秒等功率交叉淡化。
整支墊一層很低的風（−12 dB）與呼吸（−14 dB）當地板。朗讀單詞當「記憶」放在段落交接處。
小星星第一句只在 S5→S6 交接出現一次（慢速低八度、低通、很糊）。
全體過同一組殘響，再 finalize。

重跑方式（scratchpad 內）：
  source .venv/bin/activate && python agent_A/A_build.py
"""
import os, sys, math, shutil, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import collage_lib as L

ROOT, T = L.ROOT, L.TRAVEL
OUT_DIR = os.path.join(T, "拼貼試做_20260915")
TITLE = "從腳步到天空"
CODE = "A"

# ------------------------------------------------------------------ 共用參數
REVERB = dict(rt60=2.4, lp_hz=4000, predelay_ms=20, mix=0.28)   # 整支檔唯一一組空間
MASTER_LP = 7000                                                 # 整體高頻收斂
FLOOR_WIND_DB, FLOOR_BREATH_DB = -12.0, -14.0                    # 地板層相對主層

# 段長與交叉淡化（秒）
SEG_LEN = [33, 31, 33, 31, 35, 32]
XF = [7, 7, 7, 8, 9]
TOTAL = sum(SEG_LEN) - sum(XF)                                    # 157 s

CUES = []   # 設計說明用：(全域秒數, 來源檔, 處理, 層別)

def P(*parts):
    return os.path.join(*parts)

def prep(x, gain_db=0.0, lp=None, hp=None, fade_in=1.5, fade_out=1.5, lev=None, rev=False, semi=None):
    """所有素材進時間軸前的標準處理：norm −20 → 濾波 → 變速 → 短電平器 → 淡化 → 增益。"""
    if semi is not None:
        x = L.varispeed(x, semi)
    if rev:
        x = L.reverse(x)
    if hp:
        x = L.highpass(x, hp)
    if lp:
        x = L.lowpass(x, lp)
    x = L.norm_lufs(x, -20.0)
    if lev:
        x = L.leveler(x, lev[0], lev[1]); x = L.norm_lufs(x, -20.0)
    x = L.fade(x, fade_in, fade_out)
    return x * L.db(gain_db)

def seg_bus(n_s):
    return L.timeline(n_s)

def add(bus, seg_t0, x, t, gain_db=0.0, pan=0.0, src="", proc="", layer=""):
    L.place(bus, x, t, gain_db, pan)
    CUES.append((round(seg_t0 + t, 1), src, proc, layer))

# ------------------------------------------------------------------ 段落起點（全域秒數）
seg_t0 = [0]
for k in range(1, 6):
    seg_t0.append(seg_t0[-1] + SEG_LEN[k - 1] - XF[k - 1])
# seg_t0 = [0, 26, 50, 76, 99, 125]

# ================================================================== S1 步行與自行車（33 s）
def build_s1():
    n = SEG_LEN[0]; b = seg_bus(n); t0 = seg_t0[0]
    x = L.load(P(ROOT, "腳步聲素材/WindForestLeaves_SFXB.4999.wav"))
    add(b, t0, prep(L.cut(x, 5, 5 + n), 0, lp=5000, hp=120, fade_in=0.5, fade_out=3), 0, -1, 0,
        "腳步聲素材/WindForestLeaves_SFXB.4999.wav（5 到 38 s）", "高通 120 Hz、低通 5 kHz、−1 dB", "底層（林間落葉風，只在 S1）")
    x = L.load(P(ROOT, "腳步聲素材/2024聲響單車_LeavesFootsteps.wav"))
    x = L.loop_to(L.cut(x, 10, 50), n, 2.0)
    add(b, t0, prep(x, 0, lp=4500, hp=150, fade_in=0.5, fade_out=3, lev=(0.3, 8)), 0, -5, 0,
        "腳步聲素材/2024聲響單車_LeavesFootsteps.wav（10 到 50 s 循環）", "高通 150 Hz、低通 4.5 kHz、短電平器、−5 dB", "落葉步行")
    x = L.load(P(ROOT, "腳步聲素材/FootstepsLeaves_BW.7917.wav"))
    add(b, t0, prep(x, 0, lp=4500, hp=150, fade_in=1.0, fade_out=1.5, lev=(0.3, 8)), 1, -5, -0.2,
        "腳步聲素材/FootstepsLeaves_BW.7917.wav", "高通 150 Hz、低通 4.5 kHz、短電平器、−5 dB、pan −0.2", "腳步")
    x = L.load(P(ROOT, "腳步聲素材/FootstepsGravel_BW.7744.wav"))
    add(b, t0, prep(x, 0, lp=4500, hp=150, fade_in=1.5, fade_out=1.5, lev=(0.3, 8)), 7, -8, 0.2,
        "腳步聲素材/FootstepsGravel_BW.7744.wav", "高通 150 Hz、低通 4.5 kHz、短電平器、−8 dB、pan 0.2", "腳步（碎石）")
    x = L.load(P(ROOT, "腳步聲素材/FootstepsCement_BW.7554.wav"))
    add(b, t0, prep(L.cut(x, 0, 20), 0, lp=4500, hp=120, fade_in=2.0, fade_out=2.0, lev=(0.3, 8)), 14, -6, -0.1,
        "腳步聲素材/FootstepsCement_BW.7554.wav（0 到 20 s）", "高通 120 Hz、低通 4.5 kHz、短電平器、−6 dB", "腳步（水泥）")
    x = L.load(P(T, "05_自行車與步行/Bike_Pedals.wav"))
    add(b, t0, prep(x, 0, lp=6000, hp=120, fade_in=2.0, fade_out=2.0, lev=(0.4, 8)), 17, -5, 0.3,
        "05_自行車與步行/Bike_Pedals.wav", "高通 120 Hz、低通 6 kHz、短電平器、−5 dB、pan 0.3", "自行車")
    x = L.load(P(T, "05_自行車與步行/ESM_Explainer_Video_One_Shot_Foley_Bike_Wheel_Spin_Bicycle_Street_6.wav"))
    add(b, t0, prep(L.cut(x, 0, 16), 0, lp=6000, hp=120, fade_in=2.0, fade_out=3.0, lev=(0.4, 8)), 21, -5, -0.3,
        "05_自行車與步行/ESM_…_Bike_Wheel_Spin_Bicycle_Street_6.wav（0 到 16 s）", "高通 120 Hz、低通 6 kHz、短電平器、−5 dB、pan −0.3", "自行車（輪轉）")
    return L.norm_lufs(b, -20)

# ================================================================== S2 道路與城市（31 s）
def build_s2():
    n = SEG_LEN[1]; b = seg_bus(n); t0 = seg_t0[1]
    x = L.load(P(T, "03_道路與城市/Road_01.wav"))
    add(b, t0, prep(L.cut(x, 2, 2 + n), 0, lp=6000, hp=100, fade_in=2.5, fade_out=3.0), 0, -2, 0,
        "03_道路與城市/Road_01.wav（2 到 33 s）", "高通 100 Hz、低通 6 kHz、−2 dB", "底層（道路）")
    x = L.load(P(T, "03_道路與城市/CityStreet_BW.1723.wav"))
    add(b, t0, prep(L.cut(x, 40, 40 + n), 0, lp=5000, hp=100, fade_in=3.0, fade_out=3.0), 0, -4, 0,
        "03_道路與城市/CityStreet_BW.1723.wav（40 到 71 s）", "高通 100 Hz、低通 5 kHz、−4 dB", "城市（街道）")
    x = L.load(P(T, "03_道路與城市/FF_CL_ambience_london_bus_station_red.wav"))
    add(b, t0, prep(x, 0, lp=5000, hp=100, fade_in=1.5, fade_out=1.5), 9, -3, 0.3,
        "03_道路與城市/FF_CL_ambience_london_bus_station_red.wav", "高通 100 Hz、低通 5 kHz、−3 dB、pan 0.3", "城市（公車站）")
    x = L.load(P(T, "03_道路與城市/CarTurnSignal_BW.62374.wav"))
    ts = prep(x, 0, lp=2500, hp=200, fade_in=0.05, fade_out=0.5, lev=(0.3, 8))
    add(b, t0, ts, 15, -12, -0.4, "03_道路與城市/CarTurnSignal_BW.62374.wav", "高通 200 Hz、低通 2.5 kHz、短電平器、−12 dB、pan −0.4", "節拍點（方向燈）")
    add(b, t0, ts, 23, -14, 0.4, "03_道路與城市/CarTurnSignal_BW.62374.wav", "同上、−14 dB、pan 0.4", "節拍點（方向燈）")
    x = L.load(P(T, "03_道路與城市/TRFDC_Cuts_Travel_08.wav"))
    add(b, t0, prep(x, 0, lp=4000, hp=150, fade_in=0.05, fade_out=0.6, lev=(0.3, 8)), 20, -10, 0,
        "03_道路與城市/TRFDC_Cuts_Travel_08.wav", "高通 150 Hz、低通 4 kHz、短電平器、−10 dB", "短事件")
    return L.norm_lufs(b, -20)

# ================================================================== S3 火車與地鐵（33 s）
def build_s3():
    n = SEG_LEN[2]; b = seg_bus(n); t0 = seg_t0[2]
    x = L.load(P(T, "02_火車與地鐵/TrainStation_BW.51897.wav"))
    add(b, t0, prep(L.cut(x, 20, 38), 0, lp=5000, hp=80, fade_in=3.0, fade_out=4.0), 0, -3, 0,
        "02_火車與地鐵/TrainStation_BW.51897.wav（20 到 38 s）", "高通 80 Hz、低通 5 kHz、−3 dB", "車站")
    x = L.load(P(T, "02_火車與地鐵/SubwayInterior_S08TT.6.wav"))
    add(b, t0, prep(L.cut(x, 5, 5 + n), 0, lp=5000, hp=60, fade_in=3.0, fade_out=3.0), 0, -2, 0,
        "02_火車與地鐵/SubwayInterior_S08TT.6.wav（5 到 38 s）", "高通 60 Hz、低通 5 kHz、−2 dB", "底層（車廂內）")
    x = L.load(P(T, "02_火車與地鐵/FF_MT_london_underground_foley_doors_open_low_beep.wav"))
    add(b, t0, prep(x, 0, lp=3500, hp=150, fade_in=0.05, fade_out=0.4, lev=(0.3, 8)), 7, -7, 0.3,
        "02_火車與地鐵/FF_MT_london_underground_foley_doors_open_low_beep.wav", "高通 150 Hz、低通 3.5 kHz、短電平器、−7 dB、pan 0.3", "短事件（門開提示）")
    x = L.load(P(T, "02_火車與地鐵/Subway_Bart__Train_Interior_Station_Doors_Quiet_04.wav"))
    add(b, t0, prep(x, 0, lp=4500, hp=80, fade_in=0.8, fade_out=1.5, lev=(0.5, 8)), 8, -5, -0.2,
        "02_火車與地鐵/Subway_Bart__Train_Interior_Station_Doors_Quiet_04.wav", "高通 80 Hz、低通 4.5 kHz、短電平器、−5 dB、pan −0.2", "車門")
    x = L.load(P(T, "02_火車與地鐵/FF_MT_train_foley_journey_gentle.wav"))
    add(b, t0, prep(L.cut(x, 0, 24), 0, lp=5000, hp=60, fade_in=2.5, fade_out=3.0), 11, -3, 0,
        "02_火車與地鐵/FF_MT_train_foley_journey_gentle.wav（0 到 24 s）", "高通 60 Hz、低通 5 kHz、−3 dB", "行駛")
    x = L.load(P(ROOT, "其他音效素材/FF_EFX_ambience_train_passing_fast.wav"))
    add(b, t0, prep(x, 0, lp=4000, hp=80, fade_in=2.0, fade_out=2.0, lev=(0.5, 8)), 19, -5, 0.2,
        "其他音效素材/FF_EFX_ambience_train_passing_fast.wav", "高通 80 Hz、低通 4 kHz、短電平器、−5 dB、pan 0.2", "對向列車掠過")
    x = L.load(P(T, "02_火車與地鐵/TrainHornDist_SEU04.48.wav"))
    add(b, t0, prep(x, 0, lp=3000, hp=150, fade_in=0.3, fade_out=1.0, lev=(0.3, 8)), 26, -7, -0.5,
        "02_火車與地鐵/TrainHornDist_SEU04.48.wav", "高通 150 Hz、低通 3 kHz、短電平器、−7 dB、pan −0.5", "遠方汽笛")
    return L.norm_lufs(b, -20)

# ================================================================== S4 水上與船（31 s）
def build_s4():
    n = SEG_LEN[3]; b = seg_bus(n); t0 = seg_t0[3]
    x = L.load(P(T, "04_水上與船/PirateShipOceanWaves_SFXB.1.wav"))
    add(b, t0, prep(L.cut(x, 30, 30 + n), 0, lp=4500, hp=50, fade_in=3.0, fade_out=3.0), 0, -2, 0,
        "04_水上與船/PirateShipOceanWaves_SFXB.1.wav（30 到 61 s）", "高通 50 Hz、低通 4.5 kHz、−2 dB", "底層（浪）")
    x = L.load(P(T, "04_水上與船/FF_MC_foley_paddling_sea_kayak.wav"))
    add(b, t0, prep(L.cut(x, 60, 60 + n), 0, lp=4500, hp=60, fade_in=3.0, fade_out=3.0, lev=(0.3, 8)), 0, -3, -0.2,
        "04_水上與船/FF_MC_foley_paddling_sea_kayak.wav（60 到 91 s）", "高通 60 Hz、低通 4.5 kHz、短電平器、−3 dB、pan −0.2", "划槳")
    x = L.load(P(T, "04_水上與船/PaddleBoat_BW.60746.wav"))
    add(b, t0, prep(L.cut(x, 0, 16), 0, lp=4000, hp=60, fade_in=2.5, fade_out=2.5), 4, -6, 0.3,
        "04_水上與船/PaddleBoat_BW.60746.wav（0 到 16 s）", "高通 60 Hz、低通 4 kHz、−6 dB、pan 0.3", "腳踏船")
    x = L.load(P(T, "04_水上與船/PontoonBoatMedium_BW.5320.M.wav"))
    add(b, t0, prep(x, 0, lp=2500, hp=50, fade_in=3.0, fade_out=3.0, lev=(1.0, 6)), 14, -6, 0.1,
        "04_水上與船/PontoonBoatMedium_BW.5320.M.wav", "高通 50 Hz、低通 2.5 kHz、電平器、−6 dB", "船引擎")
    return L.norm_lufs(b, -20)

# ================================================================== S5 機場與起飛（35 s）
def build_s5():
    n = SEG_LEN[4]; b = seg_bus(n); t0 = seg_t0[4]
    x = L.load(P(T, "01_飛機與機場/PSE_GGV1_FX_One_Shot_Ambience_Tokyo_Airport_Departure_Lobby.wav"))
    add(b, t0, prep(L.cut(x, 0, n), 0, lp=5000, hp=60, fade_in=3.0, fade_out=4.0, lev=(0.5, 8)), 0, -2, 0,
        "01_飛機與機場/PSE_GGV1_FX_One_Shot_Ambience_Tokyo_Airport_Departure_Lobby.wav（0 到 35 s）", "高通 60 Hz、低通 5 kHz、短電平器、−2 dB", "底層（機場大廳）")
    x = L.load(P(T, "01_飛機與機場/BRS_Wheels_Luggage_Bag_OB_Roll_Heavy_1.wav"))
    add(b, t0, prep(x, 0, lp=4500, hp=80, fade_in=0.5, fade_out=1.0, lev=(0.3, 8)), 3, -6, -0.4,
        "01_飛機與機場/BRS_Wheels_Luggage_Bag_OB_Roll_Heavy_1.wav", "高通 80 Hz、低通 4.5 kHz、短電平器、−6 dB、pan −0.4", "行李箱輪子")
    x = L.load(P(T, "01_飛機與機場/BRS_Wheels_Luggage_Bag_OB_Roll_Med.wav"))
    add(b, t0, prep(x, 0, lp=4500, hp=80, fade_in=0.5, fade_out=1.0, lev=(0.3, 8)), 9, -7, 0.4,
        "01_飛機與機場/BRS_Wheels_Luggage_Bag_OB_Roll_Med.wav", "高通 80 Hz、低通 4.5 kHz、短電平器、−7 dB、pan 0.4", "行李箱輪子")
    x = L.load(P(T, "01_飛機與機場/FF_MT_airplane_foley_seatbelt_sign_dry.wav"))
    add(b, t0, prep(x, 0, lp=4000, hp=200, fade_in=0.03, fade_out=0.3, lev=(0.3, 8)), 14, -8, 0.2,
        "01_飛機與機場/FF_MT_airplane_foley_seatbelt_sign_dry.wav", "高通 200 Hz、低通 4 kHz、短電平器、−8 dB、pan 0.2", "短事件（安全帶提示）")
    x = L.load(P(T, "01_飛機與機場/BRS_Activity_Plane_Seatbelts1.wav"))
    add(b, t0, prep(L.cut(x, 10, 28), 0, lp=4500, hp=60, fade_in=2.5, fade_out=3.0, lev=(1.0, 6)), 12, -5, 0,
        "01_飛機與機場/BRS_Activity_Plane_Seatbelts1.wav（10 到 28 s）", "高通 60 Hz、低通 4.5 kHz、電平器、−5 dB", "機艙")
    x = L.load(P(T, "01_飛機與機場/FF_MT_airplane_foley_runway_riser.wav"))
    add(b, t0, prep(x, 0, lp=4500, hp=40, fade_in=2.5, fade_out=2.0, lev=(1.0, 8)), 13, -2, 0,
        "01_飛機與機場/FF_MT_airplane_foley_runway_riser.wav", "高通 40 Hz、低通 4.5 kHz、電平器（壓掉上升）、−2 dB", "跑道加速")
    x = L.load(P(T, "01_飛機與機場/JetKc135PassBy_SFXB.4295.wav"))
    add(b, t0, prep(L.cut(x, 0, 18), 0, lp=4000, hp=40, fade_in=2.5, fade_out=3.0, lev=(0.7, 8)), 20, -3, 0,
        "01_飛機與機場/JetKc135PassBy_SFXB.4295.wav（0 到 18 s）", "高通 40 Hz、低通 4 kHz、電平器、−3 dB", "噴射機掠過")
    return L.norm_lufs(b, -20)

# ================================================================== S6 風與呼吸（32 s）
def build_s6():
    n = SEG_LEN[5]; b = seg_bus(n); t0 = seg_t0[5]
    x = L.load(P(T, "06_風與空氣/FF_SFXT_foley_glacier_wind_tonal.wav"))
    add(b, t0, prep(L.loop_to(x, n, 3.0), 0, lp=4000, hp=40, fade_in=3.0, fade_out=0.5), 0, -2, 0,
        "06_風與空氣/FF_SFXT_foley_glacier_wind_tonal.wav（循環到 32 s）", "高通 40 Hz、低通 4 kHz、−2 dB", "底層（冰河風）")
    x = L.load(P(T, "06_風與空氣/ESM_Ocean_Loop_New_York_Wind_Waves_Distant_5_Deep.wav"))
    add(b, t0, prep(L.cut(x, 10, 10 + n), 0, lp=3500, hp=40, fade_in=3.0, fade_out=0.5), 0, -3, 0,
        "06_風與空氣/ESM_Ocean_Loop_New_York_Wind_Waves_Distant_5_Deep.wav（10 到 42 s）", "高通 40 Hz、低通 3.5 kHz、−3 dB", "遠方風與浪")
    x = L.load(P(ROOT, "背景pad_20260908/素材/呼吸層_平靜版_240s_loop.wav"))
    add(b, t0, prep(L.cut(x, 60, 60 + n), 0, lp=3500, hp=60, fade_in=4.0, fade_out=0.5), 0, -4, 0,
        "背景pad_20260908/素材/呼吸層_平靜版_240s_loop.wav（60 到 92 s）", "高通 60 Hz、低通 3.5 kHz、−4 dB", "呼吸（浮上來）")
    x = L.load(P(T, "06_風與空氣/FF_IE_fx_deep_wind.wav"))
    add(b, t0, prep(x, 0, lp=3000, hp=40, fade_in=1.0, fade_out=2.0, lev=(0.5, 8)), 6, -7, 0,
        "06_風與空氣/FF_IE_fx_deep_wind.wav", "高通 40 Hz、低通 3 kHz、短電平器、−7 dB", "深風")
    return L.norm_lufs(b, -20)

# ================================================================== 組合
def main():
    segs = [build_s1(), build_s2(), build_s3(), build_s4(), build_s5(), build_s6()]
    main_bus = L.xfade_concat(segs, XF)
    main_bus = main_bus[: int(TOTAL * L.SR)]
    total_s = len(main_bus) / L.SR
    master = L.timeline(total_s)
    L.place(master, main_bus, 0, 0.0)

    # ---- 地板：整支檔的風與呼吸（很低）
    wind = L.load(P(T, "06_風與空氣/ParkWindBlowAmbience_BWU.57.wav"))
    wind = prep(L.cut(wind, 0, total_s), 0, lp=2000, hp=60, fade_in=0.3, fade_out=0.3)
    L.place(master, wind, 0, FLOOR_WIND_DB)
    CUES.append((0.0, "06_風與空氣/ParkWindBlowAmbience_BWU.57.wav（0 到 157 s）", f"高通 60 Hz、低通 2 kHz、{FLOOR_WIND_DB:.0f} dB", "地板（風，全程）"))
    breath = L.load(P(ROOT, "背景pad_20260908/素材/呼吸層_平靜版_240s_loop.wav"))
    breath = prep(L.cut(breath, 0, total_s), 0, lp=3000, hp=80, fade_in=0.3, fade_out=0.3)
    L.place(master, breath, 0, FLOOR_BREATH_DB)
    CUES.append((0.0, "背景pad_20260908/素材/呼吸層_平靜版_240s_loop.wav（0 到 157 s）", f"高通 80 Hz、低通 3 kHz、{FLOOR_BREATH_DB:.0f} dB", "地板（呼吸，全程）"))

    # ---- 朗讀單詞：記憶浮出，放在段落交接處，每個接縫 1 到 2 個詞
    readers = {}
    for name in ["小軒朗讀.wav", "柏成朗讀.wav", "阿瑤朗讀.wav"]:
        y = L.load(P(ROOT, name))
        readers[name] = (y, L.phrases(L.mono(y), top_db=30))
    seams = [(seg_t0[k] + XF[k - 1] / 2) for k in range(1, 6)]   # 每個交叉淡化的中點
    plan = [  # (接縫索引, 朗讀檔, 該檔第幾個 phrase, 時間偏移, 增益, pan)
        (0, "小軒朗讀.wav", 2, -0.8, -4, -0.3),
        (1, "柏成朗讀.wav", 3, -0.5, -4, 0.3),
        (1, "阿瑤朗讀.wav", 5, 1.6, -5, -0.2),
        (2, "阿瑤朗讀.wav", 8, -0.6, -4, 0.2),
        (3, "小軒朗讀.wav", 6, -1.0, -4, 0.0),
        (3, "柏成朗讀.wav", 7, 1.4, -5, -0.4),
        (4, "阿瑤朗讀.wav", 12, -0.5, -5, 0.3),
    ]
    for si, name, idx, off, g, pan in plan:
        y, ph = readers[name]
        idx = min(idx, len(ph) - 1)
        s, e = ph[idx]
        w = prep(L.cut(y, s, e), 0, lp=2500, hp=200, fade_in=0.05, fade_out=0.25, lev=(0.3, 6))
        t = seams[si] + off
        L.place(master, w, t, g, pan)
        CUES.append((round(t, 1), f"{name}（phrase #{idx}，{s:.2f} 到 {e:.2f} s）", f"高通 200 Hz、低通 2.5 kHz、短電平器、{g} dB、pan {pan}", "記憶（朗讀單詞）"))

    # ---- 小星星第一句：只在 S5→S6 交接出現一次，慢速低八度、很糊
    tw = L.load(P(ROOT, "效果測試_20260902/00_素材切段/小星星_第一句_0.52-19.90s_原始.wav"))
    tw = prep(L.cut(tw, 0, 12), 0, lp=1200, hp=100, fade_in=3.0, fade_out=4.0, semi=-12, lev=(1.0, 6))
    t_tw = seg_t0[5] - 6
    L.place(master, tw, t_tw, -9, 0.0)
    CUES.append((round(t_tw, 1), "效果測試_20260902/00_素材切段/小星星_第一句_0.52-19.90s_原始.wav（0 到 12 s）", "變速 −12 半音（慢一倍、低八度）、高通 100 Hz、低通 1.2 kHz、電平器、−9 dB", "記憶殘影（小星星，唯一一次）"))

    # ---- 共用空間、整體高頻收斂、finalize
    y = L.reverb(master, **REVERB)[: len(master)]
    y = L.lowpass(y, MASTER_LP)
    y = L.finalize(y, tp_db=-3.5)

    dur = int(round(len(y) / L.SR))
    base = f"{CODE}_{TITLE}_{dur}s"
    wav = P(OUT_DIR, base + ".wav")
    L.write(wav, y)
    rep = L.measure(wav)
    ok = L.check(rep)
    spec = L.spectral_summary(y)

    # ---- 硬切檢查：相鄰 50 ms 視窗 RMS 跳變（頭尾 1 s 除外）
    m = L.mono(y)
    hop = int(0.05 * L.SR)
    frames = m[: (len(m) // hop) * hop].reshape(-1, hop)
    rms = 20 * np.log10(np.sqrt(np.mean(frames ** 2, axis=1)) + 1e-9)
    skip = int(1.0 / 0.05)
    d = np.abs(np.diff(rms[skip:-skip]))
    jump_max = float(d.max()); jump_at = float((np.argmax(d) + skip + 1) * 0.05)
    jump_over = int((d > 6).sum())

    report = dict(wav=wav, mp3=wav[:-4] + ".mp3", duration_s=round(len(y) / L.SR, 2), measure=rep, check=ok,
                  spectral=spec, jump50ms_max_db=round(jump_max, 2), jump50ms_at_s=round(jump_at, 2),
                  jump50ms_over6_count=jump_over, seg_t0=seg_t0, seg_len=SEG_LEN, xf=XF)
    with open(P(HERE, "A_report.json"), "w") as f:
        json.dump(report, f, ensure_ascii=False, indent=1)
    with open(P(HERE, "A_cues.json"), "w") as f:
        json.dump(sorted(CUES, key=lambda c: c[0]), f, ensure_ascii=False, indent=1)
    print(json.dumps(report, ensure_ascii=False, indent=1))

    # ---- 腳本副本
    os.makedirs(P(OUT_DIR, "scripts"), exist_ok=True)
    shutil.copy2(os.path.abspath(__file__), P(OUT_DIR, "scripts", "A_build.py"))
    return report

if __name__ == "__main__":
    main()
