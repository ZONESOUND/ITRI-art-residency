# Pressure Sensor — 雙手 FSR 握力模組

ESP32-C3 SuperMini + 2x FSR（壓力感測） + 2x WS2812 12-LED 燈圈，用於**同動車（Synchronous Movement Vehicle）的雙手握力偵測**。

> 屬於「節奏繞纏」（Rhythmic Entanglements）專案的一部分。本模組目的是讓使用者透過握力互動，引導力道控制與**雙手分離操作**——根據 Paul 在淡水義山日照中心的工作坊觀察，長者使用同動車時**傾向雙手同步用力，缺乏左右手分離控制**，所以這個模組設計上特別把兩手獨立成兩條訊號鏈，並用環狀 LED 給每隻手獨立視覺回饋。

---

## 韌體版本

目前只有一版主韌體：

| 目錄 | 板子 | 說明 |
|------|------|------|
| **`pressure_2hands/`** | ESP32-C3 SuperMini | 雙 FSR + 雙 LED ring，含 WHO protocol、自動校正、閒置待機 |

---

## 硬體接線

```
ESP32-C3 SuperMini   FSR1 (左手)     FSR2 (右手)     LED Ring 1     LED Ring 2
──────────────────   ────────────    ────────────    ──────────     ──────────
GPIO 0 (ADC) ──────  分壓中點
GPIO 1 (ADC) ─────────────────────── 分壓中點
GPIO 5 ───────────────────────────────────────────── DIN
GPIO 6 ───────────────────────────────────────────────────────── DIN
GPIO 4 ──────────── 外接按鈕（按下接 GND，觸發重新校正）
3.3V ────────────── FSR 分壓電路上端
5V (外部) ─────────────────────────────────────────── VCC ────── VCC
GND ──────────────  共地
```

> FSR 用分壓電路：FSR 一端 3.3V，另一端串一顆下拉電阻接 GND，中點接 ADC。
> WS2812 建議外接 5V 電源（板子的 3.3V 推不動 12 顆 LED）。

---

## Serial 輸出

Baud rate：**115200**

### 訊息格式（OSC 風格）

| 訊息 | 說明 |
|------|------|
| `/pressure <norm1> <norm2> <raw1> <raw2>` | 正常壓力資料（50ms 間隔，20Hz）|
| `/status calibrating <N>` | 校正倒數中（每秒一次） |
| `/status calibrated` | 校正完成 |
| `/status recalibrating` | 按鈕觸發重新校正 |
| `/status idle` | 進入閒置待機（10 秒無壓力）|
| `/status active` | 從閒置恢復 |

### `/pressure` 數值說明

| 欄位 | 型態 | 範圍 | 用途 |
|------|------|------|------|
| `norm1` / `norm2` | float | 0.000 ~ 1.000 | **控制用**（已歸零、做完上下限映射） |
| `raw1` / `raw2` | int | 0 ~ 4095 | **除錯用**（12-bit ADC 原始讀值）|

### Serial 指令

| 指令 | 功能 |
|------|------|
| `WHO\n` | 回覆 `ID:pressure`（裝置識別，給 USB Hub 分辨用） |

---

## 三段式狀態流程

```
┌──────────────┐    10 秒    ┌────────────┐    無壓 10 秒   ┌──────────┐
│   校正模式    │ ──────────→ │  正常運作   │ ─────────────→ │  閒置待機  │
│  CALIBRATING │             │   ACTIVE   │ ←───────────── │   IDLE    │
│              │             │            │   一壓就回      │            │
└──────────────┘             └────────────┘                └──────────┘
        ↑                          ↑                              │
        │                          │                              │
        └─── 按鈕（GPIO4）────────┴──────────────────────────────┘
```

### 1. 校正（10 秒）

- 開機自動進入；按鈕也會重新觸發
- 收集每個 FSR 的 min / max
- LED 燈圈：**白色呼吸燈（2 秒週期）**，sine 漸變
- 完成後計算 `zeroThreshold = min + SAFE_MARGIN`，並套 `DEFAULT_MAX = 2500` 保底（避免校正期沒人壓導致 max 太低）

### 2. 正常運作

- 每 50ms 輸出一筆 `/pressure`
- LED：**藍色亮燈，亮燈顆數 ∝ norm**（norm=0 → 1 顆，norm=1 → 12 顆）
- 動態擴展：壓超過校正 max 自動更新上限，不需要重新校正
- 按鈕：按下進入重新校正

### 3. 閒置待機（10 秒無壓力觸發）

- LED：**淡藍呼吸燈（3 秒週期）**，省電待機
- Serial 仍在輸出 `/pressure norm=0`，方便電腦端持續接收
- 任何一邊壓力 > 0 立刻恢復正常運作

---

## Max/MSP Patches

| Patch | 用途 | 推薦度 |
|-------|------|--------|
| `pressure_2hands_light.maxpat` | 輕量版，已標註 outlet（`hand1_f, hand2_f, hand1_raw, hand2_raw`） | ✅ **建議使用** |
| `pressure_2hands.maxpat` | 完整版（含視覺化等額外邏輯） | 較複雜，依需求挑選 |

### 接收鏈

```
[serial /dev/cu.usbmodem-XXXX 115200]
        ↓
    [sel 10]              ← 換行符（ASCII 10）分割訊息
        ↓
   [zl group]
        ↓
     [itoa]
        ↓
   [fromsymbol]
        ↓
  [route /pressure /status]
        ↓
[unpack 0. 0. 0 0]        ← norm1, norm2, raw1, raw2
   |    |    |  |
hand1_f hand2_f raw1 raw2
```

> 兩個 norm 是 float，所以 unpack 用 `0.`（float） 而不是 `i`（int）。

---

## 可調參數

在 `pressure_2hands.ino` 頂部：

### 校正 / 取樣

| 參數 | 預設值 | 說明 |
|------|--------|------|
| `CALIBRATION_TIME` | 10000 ms | 校正時間 |
| `SAMPLE_DELAY_MS` | 20 | ADC 取樣間隔 |
| `SAFE_MARGIN` | 80 | zeroThreshold 加在 min 上面的安全邊界 |
| `DEFAULT_MAX` | 2500 | 校正期沒人壓的保底上限 |
| `PRESSURE_OUTPUT_INTERVAL` | 50 ms | Serial 輸出頻率（20Hz）|

### 閒置偵測

| 參數 | 預設值 | 說明 |
|------|--------|------|
| `IDLE_TIMEOUT` | 10000 ms | 無壓力多久後進入閒置 |

### 校正呼吸燈（白）

| 參數 | 預設值 | 說明 |
|------|--------|------|
| `CAL_BREATHE_PERIOD` | 2000 ms | 呼吸週期 |
| `CAL_BREATHE_MIN` / `MAX` | 9 / 60 | 亮度範圍 |

### 待機呼吸燈（淡藍）

| 參數 | 預設值 | 說明 |
|------|--------|------|
| `IDLE_BREATHE_PERIOD` | 3000 ms | 呼吸週期 |
| `IDLE_BREATHE_MIN` / `MAX` | 4 / 40 | 亮度範圍 |

---

## 調整建議

| 你覺得... | 調什麼 |
|-----------|--------|
| 校正時 LED 太亮/太暗 | `CAL_BREATHE_MAX`（預設 60） |
| 待機燈太亮 | `IDLE_BREATHE_MAX`（預設 40） |
| 閒置太快進入待機 | `IDLE_TIMEOUT` 加大（預設 10 秒） |
| 輕壓無反應 | `SAFE_MARGIN` 降到 40~60（預設 80）|
| Norm 飆滿太快 | `DEFAULT_MAX` 加大（預設 2500），或重新校正用力壓 |
| 校正期沒人壓 → 之後都飆滿 | 保底已經有，但若還是怪，按按鈕重新校正 |

---

## 疑難排解

| 問題 | 可能原因 | 解法 |
|------|----------|------|
| Serial Monitor 無輸出 | ESP32-C3 未啟用 USB CDC | Tools → USB CDC On Boot → **Enabled** |
| LED 不亮或亂閃 | 5V 供電不足 | 改用獨立 5V 電源給 LED ring |
| Norm 一直是 0 | 校正期沒壓到 / `zeroThreshold` 太高 | 按按鈕重新校正，校正期間用力壓兩邊 |
| Norm 一壓就到 1.0 | `DEFAULT_MAX` 太低，或實際力道遠超預期 | 校正期間用最大力壓，讓 max 抓到真實上限 |
| Max 收到亂碼 | Baud rate 不對 | 確認 Max serial object 設 115200 |
| 兩隻手互相干擾 | 共地不確實 / FSR 分壓電路漏電 | 檢查 GND 連接、確認分壓下拉電阻 |

---

## 相依套件

- **Adafruit NeoPixel**

Arduino IDE → Library Manager → 搜尋 `Adafruit NeoPixel` 安裝。

---

## 設計脈絡（給接手的人）

這個模組不是單獨存在，是**同動車三件組之一**：

1. **TOF 距離感測** (`tof_distance_sensor/`) — XY 軸手把追蹤
2. **壓力感測**（本模組）— 雙手握力
3. **Piezo 敲擊**（`piezo_detect/piezo_4drum/`）— 第二階互動 / 雙手協調

三顆都是 ESP32-C3 SuperMini，全走 115200 Serial，全支援 `WHO\n` 指令回覆裝置 ID（`ID:pressure` / `ID:tof` / `ID:piezo`），用來在 USB Hub 多裝置時自動配對。

工作坊測試的核心發現（保羅 2026-03-27 觀察）：

- **環狀 LED 對長者很有效**——能直覺提示「需要出力」
- 旋轉 180° 會卡到電線，需要結構整理
- 長時間出力後**長者不易放鬆**——這影響了 `IDLE_TIMEOUT` 不能設太短
- **缺乏左右手分離控制**——所以 norm1/norm2 必須完全獨立輸出，不要在韌體做合併或平均

未來方向：握力可以**轉成畫筆粗細**或其他視覺變化，跟螢幕互動結合，給更明確的因果回饋。這部分留給 Max/MSP 端或 TouchDesigner 處理，本韌體只負責穩定輸出 norm1/norm2 兩條訊號。
