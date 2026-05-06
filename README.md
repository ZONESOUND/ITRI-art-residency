# ITRI Art Residency — Interactive Sensing Modules

工研院藝術進駐「**節奏繞纏**」（*Rhythmic Entanglements: Sonification Experiments on Biofeedback and Embodied Perception*）專案的程式碼。

「**同動車**」是工研院實驗室開發的**中風上肢復健輔具**，採用「好手帶壞手」連動機制——患者用健側手帶動機構、讓患側手隨動，協助動作復健。本專案在 ITRI 駐村期間跟該實驗室合作，**在同動車裝置上加裝 Pressure（壓力）／ ToF（距離）／ Piezo（壓電）三組感測器**，把使用者操作裝置時的力道、移動、敲擊轉換成即時聲響合成。

**演出主 patch 在 [`paired_motion/`](paired_motion/)。** 部署細節、系統架構、abstraction 設計都在那邊的 README。

「同動車」(literally "synchronous-motion vehicle") is an existing ITRI-developed stroke rehabilitation device using the well-hand-leads-affected-hand bimanual mechanism. This residency project, in collaboration with the device's developing lab, instruments the device with three sensors (pressure / ToF / piezo) and maps user interaction into real-time sound synthesis. **Performance master patch lives in [`paired_motion/`](paired_motion/).**

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

## 三組感測器的功能定位

每組感測器對應一種互動形式，讓使用者操作同動車時產生不同的聲響面向：

| 感測器 | 互動形式 | 訊號型態 |
|---|---|---|
| Pressure（FSR x2）| 雙手握力 | 0.0~1.0 浮點，左右獨立 |
| TOF（VL53L0X x2）| 把手 X/Y 移動位置與速度 | 距離 mm + normalized 速度 -1~1 |
| Piezo（壓電 x4） | 敲擊事件 + 連續活動串流（刮 / 摸 / 持續按壓）| velocity 1~127 + 0~1 連續強度 |

三組都接 USB Hub 進 Mac，由 Max/MSP 透過 Node.js auto-detect 配對 port，再由各自的 abstraction 處理訊號到聲響映射。

Each sensor channels a distinct interaction modality — grip force (Pressure), spatial position and velocity (ToF), strike events plus continuous activity (Piezo) — into the sonification layer.

---

## 預期使用情境 | Use Cases

- 駐村期末成果發表（工研院場域 demo、文化部訪視）
- 社區工作坊（板橋 435、淡水義山日照中心）
- 莫比斯圓環協作演出（劇場框架）
- 復健療程聽覺回饋試點
- 教學工作坊（讓參與者寫自己的 sub_*.maxpat 做聲響設計）
- 技術擴展面：加新感測器、無線通訊、多人多台同動車同步

Use cases span residency finale, community workshops, theater collaboration, rehab augmentation, and teaching workshops.

---

## WHO 裝置識別協定 | WHO Identification Protocol

同動車三件感測器接同一個 USB Hub 時，無法靠 macOS 配發的 port 編號順序辨識（順序會隨插入時機與 USB 孔變動）。三組韌體都實作了 WHO 協定：

```
電腦端 → 對每個 cu.usbmodem* 發送 "WHO\n"
ESP32 → 回覆 "ID:pressure" / "ID:tof" / "ID:piezo"
```

自動化工具：[`serial_auto_detect/`](serial_auto_detect/) — Node.js script 給 Max [node.script] 用，加上命令列診斷工具 `who_probe.js`。

When the trio shares a USB hub, port enumeration order is unstable across replug. All three firmwares implement WHO so the host can identify each device deterministically. Automated via [`serial_auto_detect/`](serial_auto_detect/).

---

## 開發環境 | Development Setup

**Mac 端 / Mac side:**
- Max/MSP 9
- Node.js 16+（給 Max [node.script] 用，含 `serialport`、`ws` 等套件）
- Python 3（早期影像偵測引擎）
- Web 端：p5.js、Web Serial API（脈搏網頁視覺）

**Arduino IDE：**
- Board 選 `ESP32C3 Dev Module`
- USB CDC On Boot 設 **`Enabled`**（同動車三件都需要，否則 Serial 走錯通道）
- 必要函式庫：`Adafruit_VL53L0X`、`Adafruit_NeoPixel`

**npm 套件安裝：** 各 Node 模組資料夾分別 `npm install`（`paired_motion/code/`、`serial_auto_detect/` 等）。
**npm:** Run `npm install` per Node module folder.

**通訊協定 / Communication:** USB Serial 115200 baud 為主、OSC-style 訊息前綴（`/tof`、`/pressure`、`/piezo`），Max 端用 `[route]` 分流。

---

## 授權 | License

MIT License. 詳見 [LICENSE](LICENSE)。
