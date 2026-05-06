# ITRI Art Residency — Interactive Sensing Modules

工研院藝術進駐「**節奏繞纏**」（*Rhythmic Entanglements: Sonification Experiments on Biofeedback and Embodied Perception*）專案的程式碼。

核心裝置為 **同動車（Synchronous Movement Vehicle）**——整合 Pressure（壓力）／ ToF（距離）／ Piezo（壓電）三件感測器的雙手互動樂器，主要面向**長者與身體感知能力較弱的使用者**。資料透過 USB Serial 進到 Max/MSP 即時聲音合成。

**演出主 patch 在 [`paired_motion/`](paired_motion/)。** 部署細節、系統架構、abstraction 設計都在那邊的 README。

This repository contains code for the *Rhythmic Entanglements* art residency project at ITRI. The flagship device is **同動車 (Synchronous Movement Vehicle)** — a two-hand interactive musical instrument bundling pressure, ToF, and piezoelectric sensors, designed for elderly and embodiment-impaired users. **Performance master patch lives in [`paired_motion/`](paired_motion/).**

---

## 資料夾結構 | Repository Structure

### 🚗 同動車三件感測器 | The 同動車 Trio

接同一個 USB Hub，全部使用 ESP32-C3 SuperMini，115200 baud，皆支援 WHO 裝置識別協定。

| 資料夾 | 說明 | WHO ID |
|---|---|---|
| [`pressure_sensor/`](pressure_sensor/) | 雙手 FSR 握力感測 + WS2812 LED ring 視覺回饋 | `pressure` |
| [`tof_distance_sensor/`](tof_distance_sensor/) | 雙 VL53L0X ToF 感測器追蹤把手 X/Y 位置與速度 | `tof` |
| [`piezo_detect/`](piezo_detect/) | 4 通道壓電偵測（4-drum），同時提供敲擊事件與連續活動串流 | `piezo` |

### 🎭 同動車演出整合 | Performance Integration

| 資料夾 | 說明 |
|---|---|
| **[`paired_motion/`](paired_motion/)** | **演出主 patch** —— Max Project 自包含結構，含主 patch、四個感測器處理 abstractions、聲響素材、Cycling74 vs library + PeRColate externals。zip 整包帶到別台電腦跑 |

### 🔧 同動車的支援工具 | Supporting Tooling

| 資料夾 | 說明 |
|---|---|
| [`serial_auto_detect/`](serial_auto_detect/) | Mac 端自動掃描 USB port + WHO 握手 + 餵 port 名給 Max [serial]。`paired_motion/code/` 是這支工具的凍結副本 |

### 📐 模板 | Templates

| 檔案 | 說明 |
|---|---|
| [`arduino_template.maxpat`](arduino_template.maxpat) | 通用 Arduino-over-Serial 接收 patch 範本，**跟具體感測器無關**。新接一顆 Arduino 不知道從哪開始就拿這個改 |

### 🧪 開發歷程中的其他模組 | Phased Development Outputs

下列模組是駐村期間不同階段的探索與獨立子專案。**目前未必整合進 `paired_motion/` 演出版本**，但各自完成過某個階段任務（演出、工作坊、技術探索），保留作為日後迭代的素材。

| 資料夾 | 說明 |
|---|---|
| [`breath_sensor/`](breath_sensor/) | 吹氣樂器：HX710B + 超音波霧化器 + WS2812 燈圈動畫 |
| [`duo_pulse_sonification/`](duo_pulse_sonification/) | 雙人脈搏聲音化（p5.js Lissajous + Web Serial API） |
| [`piezo_detect_fft/`](piezo_detect_fft/) | 壓電 FFT 頻譜分析（hit / scrub 事件偵測） |
| [`local_mediapipe/`](local_mediapipe/) | 本地端 MediaPipe 手部追蹤（為 LA Life in Motion 演出開發） |
| [`remote_hand_tracking/`](remote_hand_tracking/) | 透過 WebSocket 從遠端機器接收手部追蹤資料 |
| [`legacy_local_cv_engine/`](legacy_local_cv_engine/) | 早期版本的 Python OpenCV 動態偵測引擎（已被 local_mediapipe 取代） |

各資料夾自帶 README，有實作細節跟使用方式。

---

## 設計構想 | Design Concept

「同動車」名字來自 Paul（合作藝術家）在**淡水義山日照中心**工作坊的觀察：**長者操作雙手互動裝置時，左右手傾向同步用力**，缺乏左右分離控制的能力。這個「同動」現象既是症狀（運動控制功能下降）也是契機（能設計引導左右手分工的互動）。

paired_motion 的設計圍繞三個面向：

1. **三種互動形式並行**——握（Pressure）、距離移動（TOF）、敲擊與刮（Piezo），讓使用者一次體驗三種身體感知模式的差異
2. **左右分離設計**——Pressure 明確分左右獨立訊號鏈，TOF 雙感測器追蹤 X/Y 軸，**鼓勵使用者意識到左右手在做不同的事**
3. **多重視覺與聽覺回饋**——每組感測器都有對應 LED + 即時聲響映射，從感官回饋學會精細控制

The name "同動車" (literally "same-motion vehicle") came from observing how elderly users tend to move both hands in sync, lacking independent left/right control. This synchronization is both a symptom of declining motor control AND an opportunity — to design interactions that guide users toward bimanual differentiation.

---

## 未來應用 | Future Applications

paired_motion 不是一次性演出 patch，是一套**可擴展的互動聲響平台**。預期使用方向：

- **駐村期末成果發表** — 工研院場域 demo + 文化部訪視
- **社區工作坊延伸** — 板橋 435、淡水義山日照中心，讓長者親身操作 + 共同創作
- **跟莫比斯圓環協作演出** — 劇場框架下的敘事 + 互動結合
- **老人照護 / 復健場域試點** — 從互動裝置變成感官評估工具
- **教學工作坊** — 讓參與者寫自己的 abstraction（sub_*.maxpat）做聲響設計

技術擴展面：加新感測器（再寫一支 sub_xxx）、無線版本（WiFi/OSC 取代 USB）、多點同步（多人多台同動車）。

---

## WHO 裝置識別協定 | WHO Identification Protocol

同動車三件感測器接同一個 USB Hub 時，無法靠 macOS 配發的 port 編號順序辨識（順序會隨插入時機與 USB 孔變動）。三組韌體都實作了 WHO 協定：

```
電腦端 → 對每個 cu.usbmodem* 發送 "WHO\n"
ESP32 → 回覆 "ID:pressure" / "ID:tof" / "ID:piezo"
```

自動化工具：[`serial_auto_detect/`](serial_auto_detect/) — Node.js script 給 Max [node.script] 用，加上命令列診斷工具 `who_probe.js`。

---

## 開發環境 | Development Setup

**Mac 端：**
- Max/MSP 9
- Node.js 16+（給 Max [node.script] 用，含 `serialport`、`ws` 等套件）
- Python 3（早期影像偵測引擎）
- Web 端：p5.js、Web Serial API（脈搏網頁視覺）

**Arduino IDE：**
- Board 選 `ESP32C3 Dev Module`
- USB CDC On Boot 設 **`Enabled`**（同動車三件都需要，否則 Serial 走錯通道）
- 必要函式庫：`Adafruit_VL53L0X`、`Adafruit_NeoPixel`

**npm 套件安裝：** 各 Node 模組資料夾分別 `npm install`（`paired_motion/code/`、`serial_auto_detect/` 等）。

**通訊協定：** USB Serial 115200 baud 為主、OSC-style 訊息前綴（`/tof`、`/pressure`、`/piezo`），Max 端用 `[route]` 分流。

---

## 授權 | License

MIT License. 詳見 [LICENSE](LICENSE)。
