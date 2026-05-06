# ITRI Art Residency — Interactive Sensing Modules

工研院藝術進駐「**節奏繞纏**」（*Rhythmic Entanglements: Sonification Experiments on Biofeedback and Embodied Perception*）專案的程式碼。

核心裝置為 **同動車（Synchronous Movement Vehicle）**——整合 Pressure（壓力）／ ToF（距離）／ Piezo（壓電）三件感測器的雙手互動樂器，主要面向**長者與身體感知能力較弱的使用者**。資料透過 USB Serial 進到 Max/MSP 即時聲音合成，演出主 patch 在 [`paired_motion/`](paired_motion/)。

This repository contains code for the *Rhythmic Entanglements* art residency project at ITRI (Industrial Technology Research Institute, Taiwan). The flagship device is the **同動車 (Synchronous Movement Vehicle)** — a two-hand interactive musical instrument bundling pressure, time-of-flight distance, and piezoelectric sensors, designed for elderly and embodiment-impaired users. Sensor data is streamed over USB serial into Max/MSP. The performance master patch lives in [`paired_motion/`](paired_motion/).

---

## 資料夾結構 | Repository Structure

### 🚗 同動車三件感測器 | The 同動車 Trio

接同一個 USB Hub、全部使用 ESP32-C3 SuperMini、115200 baud、皆支援 WHO 裝置識別協定。

All three connect to a shared USB Hub, run on ESP32-C3 SuperMini at 115200 baud, and implement the WHO identification protocol.

| 資料夾 | 中文 | English | WHO ID |
|---|---|---|---|
| [`pressure_sensor/`](pressure_sensor/) | 雙手 FSR（Force Sensitive Resistor）握力感測 + WS2812 LED ring 視覺回饋 | Dual-FSR grip-force sensing with LED ring feedback | `pressure` |
| [`tof_distance_sensor/`](tof_distance_sensor/) | 雙 VL53L0X ToF 感測器追蹤把手 X/Y 位置與速度 | Dual VL53L0X ToF tracking with X/Y position and velocity | `tof` |
| [`piezo_detect/`](piezo_detect/) | 4 通道壓電敲擊偵測（4-drum），同時提供敲擊事件與連續活動串流 | 4-channel piezoelectric strike detection with both discrete hits and continuous activity stream | `piezo` |

### 🎭 同動車演出整合 | Performance Integration

| 資料夾 | 用途 | Purpose |
|---|---|---|
| **[`paired_motion/`](paired_motion/)** | **演出主 patch**（同動車三組感測器整合）—— Max Project，含主 patch、各感測器處理 abstractions、聲響素材、Cycling74 vs library + PeRColate externals。zip 可整包帶到別台電腦跑 | **Performance master patch** — Max Project bundling main patch, per-sensor abstractions, audio assets, and consolidated dependencies. Zip-portable to other machines |

### 🔧 同動車的支援工具 | Supporting Tooling for the 同動車

| 資料夾 | 用途 | Purpose |
|---|---|---|
| [`serial_auto_detect/`](serial_auto_detect/) | Mac 端自動掃描 USB port + WHO 握手 + 餵 port 名給 Max [serial]，免手動配對。`paired_motion/` 用的就是這套機制（凍結副本在 `paired_motion/code/`） | Auto-scans USB ports, runs WHO handshake, feeds matched port names to Max [serial]. The mechanism `paired_motion/` uses (frozen copy in `paired_motion/code/`) |

### 📐 模板 | Templates

| 檔案 | 用途 | Purpose |
|---|---|---|
| [`arduino_template.maxpat`](arduino_template.maxpat) | 通用的 Arduino-over-Serial 接收 patch 範本（umenu 選 port + metro polling + sel/zl group/itoa/fromsymbol 解析鏈），跟具體感測器無關。**新接一顆 Arduino 不知道從哪開始**時拿這個改 | Generic Arduino-over-Serial receiver template (port dropdown + metro polling + standard parsing chain). Sensor-agnostic — copy and adapt when bringing in a new Arduino |

### 🧪 開發歷程中的其他模組 | Phased Development Outputs

下列模組是駐村期間不同階段的探索成果與獨立子專案。**目前未必整合進 `paired_motion/` 演出版本**，但各自完成過某個階段任務（演出、工作坊、技術探索），保留下來作為日後迭代的素材。

The following are independent sub-projects developed at different phases of the residency. **Not necessarily integrated into the current `paired_motion/` performance**, but each fulfilled a specific past task (performance, workshop, technical exploration) and is kept as material for future iterations.

| 資料夾 | 中文 | English |
|---|---|---|
| [`breath_sensor/`](breath_sensor/) | 吹氣樂器：HX710B 壓力感測 + 超音波霧化器 PWM + WS2812 燈圈動畫 | Breath instrument: HX710B + ultrasonic mister PWM + animated LED ring |
| [`duo_pulse_sonification/`](duo_pulse_sonification/) | 雙人脈搏聲音化（Lissajous 視覺化、Web Serial API 網頁端） | Dual-participant pulse sonification with Lissajous visuals and Web Serial API |
| [`piezo_detect_fft/`](piezo_detect_fft/) | 壓電 FFT 頻譜分析（hit / scrub 事件偵測） | Piezo FFT spectrum analyzer with hit / scrub event detection |
| [`local_mediapipe/`](local_mediapipe/) | 本地端 MediaPipe 手部追蹤（含網頁與 Max 整合） | Local MediaPipe hand tracking with web and Max integration |
| [`remote_hand_tracking/`](remote_hand_tracking/) | 透過 WebSocket 從遠端機器接收手部追蹤資料 | WebSocket-based remote hand tracking receiver |
| [`legacy_local_cv_engine/`](legacy_local_cv_engine/) | 早期版本的 Python OpenCV 動態偵測引擎 | Legacy Python OpenCV motion detection engine |

---

## 演出整合：paired_motion 詳細介紹 | Performance Integration: paired_motion in Detail

### 設計構想 | Design Concept

「同動車」名字來自一個觀察：Paul（駐村合作藝術家）在**淡水義山日照中心**進行的工作坊裡發現，**長者操作雙手互動裝置時，左右手傾向同步用力**，缺乏左右分離控制的能力。這個「同動」現象既是限制（運動控制功能下降的症狀）也是契機（能設計引導左右手分工的互動）。

paired_motion 的整體設計圍繞三個面向：

1. **三種互動形式並行**——握（Pressure）、距離移動（TOF）、敲擊與刮（Piezo），讓使用者在同一個裝置上體驗三種**身體感知模式**的差異。每種感測器對應不同的物理動作詞彙
2. **左右分離設計**——Pressure 模組明確分成左手 / 右手兩條獨立訊號鏈，TOF 雙感測器一個追蹤 X 一個追蹤 Y，鼓勵使用者**意識到左右手在做不同的事**
3. **多重視覺與聽覺回饋**——每組感測器都有對應的 LED 視覺回饋（呼吸燈、活動指示燈），加上即時的聲響映射，讓使用者**從感官回饋學會精細控制**

The name "同動車" (literally "same-motion vehicle") came from observing how elderly users in a Tamsui daycare workshop tended to move both hands in sync, lacking independent left/right control. This synchronization is both a symptom of declining motor control AND an opportunity — to design interactions that guide users toward bimanual differentiation.

### 系統架構 | System Architecture

```
┌─────────────── 硬體層 / Hardware ──────────────┐
│                                                │
│  ESP32-C3 #1   ESP32-C3 #2   ESP32-C3 #3      │
│  (Pressure)    (TOF)         (Piezo 4-drum)   │
│   ├ FSR x2      ├ VL53L0X x2  ├ Piezo x4      │
│   └ LED ring x2 └ Button+LED  └ LED x4        │
│        │            │              │           │
│        └─── USB Hub ─── Mac                   │
│                                                │
└────────────────────────────────────────────────┘
                       │
                       ▼
┌──────── Mac 端 / Max/MSP 9 + Node.js ─────────┐
│                                                │
│  paired_motion.maxproj                        │
│       ↓                                        │
│  patchers/main.maxpat                         │
│       │                                        │
│       ├─ [bpatcher sub_auto_detect]           │
│       │     │                                  │
│       │     └─ node.script auto_detect.js     │
│       │       ↓ (掃描 + WHO 握手)               │
│       │     [serial a/b/c] x 3                 │
│       │       ↓ (依韌體前綴 route 分流)          │
│       │     /tof  /pressure  /piezo  ...      │
│       │                                        │
│       ├─ [bpatcher sub_tof]      → 聲響 A      │
│       ├─ [bpatcher sub_pressure] → 聲響 B      │
│       ├─ [bpatcher sub_piezo]    → 聲響 C      │
│       │                                        │
│       └─ [混音] → [dac~] → 喇叭                 │
│                                                │
└────────────────────────────────────────────────┘
```

每個 abstraction（`sub_*`）負責**一種感測器的訊號處理 + 聲響映射**，主 patch 只做**佈線、整合、混音**。這種分層讓單一感測器的聲音設計能獨立調整、debug，不會牽動其他組。

### 未來應用 | Future Applications

paired_motion 不是一次性演出 patch，是一套**可擴展的互動聲響平台**。預期使用方向：

- **駐村期末成果發表**——核心使用情境，工研院場域 demo + 文化部訪視
- **社區工作坊延伸**——板橋 435、淡水義山日照中心等場域，讓長者親身操作 + 共同創作。後續可能加上**錄製功能**（紀錄受訪者的聲響表現）
- **跟莫比斯圓環協作演出**——劇場框架下的敘事 + 互動結合，可能需要 patch 增加**演出腳本控制層**（時間軸、段落切換）
- **老人照護 / 復健場域試點**——從互動裝置變成**感官評估工具**，紀錄左右手分離度、反應時間、力道變化等指標
- **未來教學工作坊**——讓參與者試試自己**寫 abstraction**（sub_*.maxpat），把同動車當成 Max 教學的具體案例

技術擴展面：

- **加入新感測器**——既有 abstraction 框架可吸收（再寫一支 sub_xxx.maxpat 對應）
- **無線版本**——韌體加 WiFi/OSC 取代 USB Serial（serial_auto_detect 之外的另一套通訊）
- **多點同步**——多人同時操作多台同動車，演出規模放大

詳細部署、abstraction 設計、port 對應等實作細節在 [`paired_motion/README.md`](paired_motion/README.md)。

---

## 主要使用的工具與函式庫 | Tools and Libraries

**ESP32 韌體 | Microcontroller firmware**
- ESP32 / ESP32-C3 SuperMini（同動車三件統一使用 ESP32-C3）
- Arduino IDE 2.x，附加套件：
  - `Adafruit_VL53L0X`（ToF 感測器驅動）
  - `Adafruit_NeoPixel`（WS2812 LED ring 控制）

**感測元件 | Sensors**
- FSR（Force Sensitive Resistor，壓力感測）
- VL53L0X（飛時測距 ToF 模組）
- Piezo（壓電片，敲擊與連續活動偵測）
- HX710B（壓差訊號放大，用於吹氣感測）
- Pulse Sensor（PPG 光學脈搏感測）

**Mac 端軟體 | Software on Mac**
- Max/MSP 9（互動聲音合成，主要展演平台）
- Node.js 16+（給 Max [node.script] 用，含 `serialport`、`ws` 等套件）
- Python 3（早期影像偵測引擎，OpenCV）
- Web 端：p5.js、Web Serial API（用於脈搏網頁視覺）
- MediaPipe（手部關鍵點追蹤）

**通訊協定 | Communication**
- USB Serial（115200 baud 為主，piezo 8 kHz raw stream 版本用 921600 baud）
- WebSocket（遠端手部追蹤）
- OSC-style 訊息前綴（`/tof`、`/pressure`、`/piezo` 等，所有 Serial 輸出都加前綴讓 Max 端用 `[route]` 分流）

---

## 硬體 | Hardware

**同動車三件 | The 同動車 Trio**
- ESP32-C3 SuperMini × 3
- FSR 壓力感測器 × 2（接 Pressure 那顆）
- VL53L0X ToF 模組 × 2（接 TOF 那顆）
- 壓電片 × 4（接 Piezo 4-drum）
- WS2812 12-LED 燈圈 × 2（接 Pressure 那顆做視覺回饋）
- LED × 4（接 Piezo 4-drum，每個通道一顆敲擊指示燈）
- USB Hub（三顆 ESP32 集中管理）

**獨立模組需要的額外硬體 | Additional hardware for standalone modules**
- ESP32 × 1（呼吸模組）：HX710B + 超音波霧化器 + WS2812 12-LED 燈圈
- ESP32 × 1（脈搏模組）：Pulse Sensor × 2、PPG 紅外 LED + 光感二極體
- 壓電片 × 1 + 5.1 kΩ 或 1 MΩ 並聯電阻（給單通道 8 kHz raw stream 版本）
- 網路攝影機（手部追蹤模組用）

---

## WHO 裝置識別協定 | WHO Identification Protocol

同動車三件感測器接同一個 USB Hub 時，無法靠 macOS 配發的 port 編號順序辨識，因為**順序會隨插入時機與 USB 孔變動**。三組韌體都實作了 WHO 協定：

When the 同動車 modules share a USB Hub, port enumeration order is unstable across replug. All three firmwares implement WHO so that the host can identify each device deterministically.

```
電腦端 → 對每個 cu.usbmodem* 發送 "WHO\n"
ESP32 → 回覆 "ID:pressure" / "ID:tof" / "ID:piezo"
```

**自動化工具**：[`serial_auto_detect/`](serial_auto_detect/) 提供 Node.js 端的 auto-detect 腳本（給 Max [node.script] 用）以及命令列診斷工具。詳見 [serial_auto_detect/README.md](serial_auto_detect/README.md)。

---

## 各模組說明 | Module Details

### pressure_sensor 🚗

雙 FSR 加雙 WS2812 LED 燈圈的雙手握力模組。10 秒自動校正、閒置呼吸燈待機、按鈕觸發重新校正。輸出格式 `/pressure norm1 norm2 raw1 raw2`（norm 為 0.0~1.0 浮點，raw 為 ADC 整數）。同動車三件之一。詳見 [`pressure_sensor/README.md`](pressure_sensor/README.md)。

Dual-FSR + dual-LED-ring grip-force module with auto-calibration, idle breathing standby, and button-triggered recalibration.

### tof_distance_sensor 🚗

雙 VL53L0X ToF 感測器追蹤同動車把手的 X / Y 位置，用三層濾波（中位數、自適應 EMA、Deadband）+ 速度計算（停下立刻歸零，無慣性尾巴）。提供三種視覺化路線：Max 內建 GL 線條繪製、pictslider 顯示、網頁 Canvas（軌跡與熱圖）。詳見 [`tof_distance_sensor/README.md`](tof_distance_sensor/README.md)。

Dual VL53L0X ToF tracking with three-layer filtering and velocity output that snaps to zero when stationary.

### piezo_detect 🚗

4 通道壓電敲擊偵測（4-drum）。動態 baseline 追蹤、IIR 濾波、連續超過門檻 debounce、non-blocking peak capture。每個通道一顆 LED 視覺回饋。**同時提供兩種輸出**：

- **離散事件**：`/piezo channel velocity rawPeak`（敲擊瞬間觸發）
- **連續活動串流**：`/piezo/stream d1 d2 d3 d4`（50 Hz，4 通道當下活動量）

設計分工是「敲」用事件、「刮／摸」用連續串流。詳見 [`piezo_detect/piezo_4drum/README.md`](piezo_detect/piezo_4drum/README.md)。

4-channel piezo strike detection with dual output: discrete hit events plus continuous activity stream for scratch / touch detection.

### paired_motion 🎭

同動車三組感測器的演出整合，Max Project 自包含結構（main + abstractions + samples + externals）。

設計構想、系統架構、未來應用見上方 [演出整合：paired_motion 詳細介紹](#演出整合paired_motion-詳細介紹--performance-integration-paired_motion-in-detail)。實作部署細節、abstraction 設計、port 對應、git tag 還原機制等在 [`paired_motion/README.md`](paired_motion/README.md)。

### serial_auto_detect 🔧

同動車三件 Serial Port 自動辨識工具（debug / 開發環境）。

包含：
- `auto_detect.js`：Max [node.script] 用的主邏輯，自動掃描 USB port 並透過 WHO 協定配對
- `who_probe.js`：命令列單 port 診斷工具（不需要 Max）
- `auto_detect_test.maxpat`：Max 端 wiring 範例

解決的問題：三顆 ESP32 接 USB Hub 時 port 順序不固定，patch 寫死容易在演出前出錯。`paired_motion/code/` 是這支工具的凍結副本，這邊則是還在迭代的開發版本。詳見 [`serial_auto_detect/README.md`](serial_auto_detect/README.md)。

Auto-detection toolkit for the 同動車 trio (dev / debug): scans USB ports, runs WHO handshake, feeds matched port names back to Max.

### arduino_template.maxpat 📐

通用的 Arduino-over-Serial 接收 patch 範本，**跟具體感測器無關**。

物件組成：`[loadbang]` → `[p devices]`（列舉 serial port 給 umenu 選）→ `[p createMenu]` → `[prepend port]` → `[serial f 115200 8 1 0]` → `[sel 10]` → `[zl group 1000]` → `[itoa]` → `[fromsymbol]`，配上 `[metro 33]` 作為 polling driver。

什麼時候用：**新接一顆 Arduino 不知道從哪開始**。複製這份 patch 改一下 baud rate 跟下游 `[route]` 比對的訊息前綴就能跑。**它不是同動車相關的工具**，是個獨立的入門範本。

A generic, sensor-agnostic Arduino-over-Serial receiver template patch. Useful when bringing in a new Arduino and you don't want to wire from scratch.

### breath_sensor 🧪

HX710B 吹氣／吸氣感測 + 超音波霧化器 PWM 控制 + WS2812 LED 動畫（旋轉白點，隨吹氣強度指數加速、動態調整尾長）+ ToF 距離決定底色色溫。最新版本：[`breath_sensor/breath_0115_c3/`](breath_sensor/breath_0115_c3/)（ESP32-C3 SuperMini）。

**階段定位**：駐村中段獨立發展的吹氣樂器原型。**目前未整合進 paired_motion**，但機制可作為將來「同動車 + 呼吸」延伸版本的素材。

### duo_pulse_sonification 🧪

雙人脈搏互動系統，同時擷取兩位參與者的心跳。三段式自動校準演算法（v2.4）輸出 BPM、心跳觸發訊號、手指接觸狀態。附 `heartbeats-harmony.html`：以 p5.js 繪製沙畫式 Lissajous 圖形，支援 Web Serial API 直接從 Chrome 讀取 ESP32 資料。

**階段定位**：駐村期間為了**雙人共構**這個概念做的探索（兩個身體訊號互相對應）。**目前未整合進 paired_motion**，是獨立的成果展示作品。

### piezo_detect_fft 🧪

壓電 FFT 頻譜分析器（I2S ADC 16 kHz 取樣，1024 點 FFT，32 個對數頻帶）。內建 hit（突發打擊）與 scrub（高頻摩擦）兩種事件偵測。

**階段定位**：壓電訊號的進階特徵分析探索。**目前 paired_motion 的 piezo_4drum 用更輕量的時域偵測，這個 FFT 版本沒被選用**。但如果未來想做「敲擊分類」（區分敲擊不同位置 / 不同物件）這層工具還在。

### local_mediapipe 🧪

使用 MediaPipe 在本地端做手部追蹤，整合 Max/MSP 與網頁視覺化。包含 `2hands_mediapipe.maxpat`（為 LA Music Center 的 *Life in Motion* 演出開發的雙手追蹤）。

**階段定位**：為**美國 LA Life in Motion 演出**開發的影像感測模組（駐村以外的相關演出）。**跟工研院同動車不同主軸**，但代碼共存於這個 repo 因為都在處理「身體動作 → 聲響」這個共通主題。

### remote_hand_tracking 🧪

透過 WebSocket 從遠端機器接收 MediaPipe 手部追蹤資料。

**階段定位**：探索「另一台電腦做影像處理、把結果送到 Max」這種分散式架構，配合 [`local_mediapipe/`](local_mediapipe/) 的 server 端。**目前未整合進任何演出**。

### legacy_local_cv_engine 🧪

早期版本的本地影像動態偵測引擎，使用 Python OpenCV，由 Max/MSP 透過 Node.js 腳本啟動。

**階段定位**：駐村**最早期**的影像實驗，已被 `local_mediapipe/`（更輕量、跨平台）取代。保留作為 OpenCV motion detection 範例。

---

## 開發環境 | Development Setup

### Mac 端

```bash
# Node.js 版本（給 Max [node.script] 與 serial_auto_detect 用）
nvm install 20
nvm use 20

# 各 Node 模組資料夾分別執行
cd serial_auto_detect && npm install
cd duo_pulse_sonification/ws_osc_relay && npm install
# ... 以此類推
```

### Arduino IDE

- 安裝 ESP32 開發板支援（Boards Manager → 搜尋 ESP32 → Espressif Systems）
- Board 選 `ESP32C3 Dev Module`
- USB CDC On Boot 設 `Enabled`（同動車三件都需要）
- 必要函式庫：`Adafruit_VL53L0X`、`Adafruit_NeoPixel`

---

## 授權 | License

MIT License. 詳見 [LICENSE](LICENSE)。
