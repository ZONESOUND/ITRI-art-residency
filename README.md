# ITRI Art Residency - Interactive Sensing Modules

## 專案簡介 | Project Overview

工研院藝術進駐「**節奏繞纏**」（Rhythmic Entanglements）專案的程式碼倉庫。結合多種互動感測技術（壓力、ToF 距離、壓電敲擊、吹氣、脈搏、手部追蹤），透過 ESP32 微控制器擷取感測數據，以 Max/MSP、Python、WebSocket 等技術串接，實現即時互動藝術裝置。核心裝置為 **同動車（Synchronous Movement Vehicle）**——整合壓力 / ToF / Piezo 三件感測器的雙手互動樂器。

An art residency project at ITRI (*Rhythmic Entanglements: Sonification Experiments on Biofeedback and Embodied Perception*). Combines pressure, ToF distance, piezoelectric, breath, pulse, and hand-tracking sensors via ESP32, Max/MSP, Python, and WebSocket. The flagship device is the **同動車 (Synchronous Movement Vehicle)** — a two-hand interactive musical instrument bundling pressure, ToF, and piezo modules.

---

## 專案架構 | Project Structure

**🚗 同動車三件組（USB Hub 集中管理，全部 ESP32-C3 SuperMini，全支援 WHO 識別協定）：**

| Directory | 中文說明 | Description | WHO ID |
|---|---|---|---|
| `pressure_sensor/` | 雙手 FSR 握力模組（含 LED ring 視覺回饋） | Dual-FSR grip-force module with LED ring feedback | `pressure` |
| `tof_distance_sensor/` | 雙 VL53L0X XY 軸把手追蹤 | Dual VL53L0X XY-axis handle tracking | `tof` |
| `piezo_detect/` | 4 通道壓電敲擊偵測（4-drum） | 4-channel piezo strike detection | `piezo` |

**獨立模組 | Standalone Modules：**

| Directory | 中文說明 | Description |
|---|---|---|
| `breath_sensor/` | 吹氣樂器（HX710B + 霧化器 PWM + LED ring 動畫） | Breath instrument: HX710B + mister PWM + animated LED ring |
| `duo_pulse_sonification/` | 雙人脈搏聲音化（Lissajous + p5.js Web Serial） | Dual-pulse sonification with Lissajous + p5.js Web Serial |
| `piezo_detect_who/` | 單通道 8kHz 壓電原始波形串流（給 FluCoMa/MuBu 特徵抽取用） | Single-channel 8kHz raw piezo stream for FluCoMa/MuBu feature extraction |
| `piezo_detect_fft/` | 壓電 FFT 頻譜分析（hit / scrub 偵測） | Piezo FFT analysis with hit / scrub event detection |
| `local_mediapipe/` | 本地端 MediaPipe 手部追蹤 | Local MediaPipe hand tracking |
| `remote_hand_tracking/` | 遠端手部追蹤（WebSocket） | Remote hand tracking via WebSocket |
| `legacy_local_cv_engine/` | 初版本地影像動態偵測引擎 | Legacy local computer vision engine |

---

## 技術棧 | Tech Stack

- **Microcontroller**: ESP32 / ESP32-C3 SuperMini（同動車三件組統一使用）
- **Sensing**: FSR, ToF (VL53L0X), Piezoelectric, HX710B (Breath), Pulse Sensor (PPG)
- **Software**: Max/MSP, Python, JavaScript (Node.js, p5.js)
- **Communication**: Serial（115200 / 921600 baud）, WebSocket, OSC, Web Serial API
- **Computer Vision**: MediaPipe (Hand Tracking)

## 硬體需求 | Hardware Requirements

- ESP32-C3 SuperMini x N（同動車三件組各 1）+ 額外 ESP32 給呼吸/脈搏 / x N ESP32-C3 SuperMini for the 同動車 trio + extra ESP32 for breath/pulse
- FSR 壓力感測器 x 2 / FSR pressure sensors x 2
- VL53L0X ToF x 2 / VL53L0X ToF sensors x 2
- 壓電片 x 4（4-drum）/ x 1（8kHz stream）/ Piezo discs x 4 (4-drum) / x 1 (stream)
- HX710B（吹氣）+ 霧化器 + WS2812 12-LED ring / HX710B (breath) + ultrasonic mister + WS2812 12-LED ring
- 脈搏感測器 x 2（PPG IR LED + Photodiode）/ Pulse Sensors x 2
- WS2812 12-LED ring x N（給壓力 / 吹氣模組）/ WS2812 12-LED rings for pressure / breath modules
- USB Hub（同動車三件感測器集中管理）/ USB Hub for the 同動車 trio
- 網路攝影機（手部追蹤用）/ Webcam (for hand tracking)

### WHO 裝置識別協定 | WHO Identification Protocol

同動車三件感測器接同一個 USB Hub 時無法靠 port 順序辨識，因此**所有同動車模組韌體都實作了 WHO 協定**：

When the 同動車 modules share a USB Hub, they're indistinguishable by port order. **All 同動車 firmware implements a WHO protocol** for identification:

```
電腦端 → 對每個 cu.usbmodem* 發送 "WHO\n"
ESP32 → 回覆 "ID:pressure" / "ID:tof" / "ID:piezo"
```

⚠️ `piezo_detect_who/` 也回 `ID:piezo`，與 `piezo_4drum/` 衝突——若同時使用兩種 piezo 韌體，需在韌體內手動修改 `DEVICE_ID`。

## 各模組簡述 | Module Details

### pressure_sensor 🚗
雙 FSR + 雙 WS2812 LED Ring 的雙手握力模組，10 秒自動校正、閒置呼吸燈待機、按鈕重新校正。輸出 `/pressure norm1 norm2 raw1 raw2`（norm 為 0.0~1.0 浮點）。同動車三件組之一。詳見 [`pressure_sensor/README.md`](pressure_sensor/README.md)。
Dual-FSR + dual-LED-ring grip-force module with auto-calibration, idle breathing standby, and button recalibrate. One of the 同動車 trio.

### tof_distance_sensor 🚗
雙 VL53L0X ToF 感測器追蹤同動車把手 X/Y 位置，三層濾波（Median + 自適應 EMA + Deadband）+ 速度輸出（停下立刻歸零，無慣性尾巴）。提供三種視覺化路線：Max GL 線條繪製、pictslider 顯示、網頁 Canvas（Trail/Heatmap）。詳見 [`tof_distance_sensor/README.md`](tof_distance_sensor/README.md)。
Dual VL53L0X ToF tracking with three-layer filtering and velocity output (snaps to 0 when stationary). Three visualization paths: Max GL, pictslider, and web Canvas.

### piezo_detect 🚗
4 通道壓電敲擊偵測（4-drum），動態 baseline + IIR 濾波 + 連續超門檻 debounce + non-blocking peak capture。每通道對應一顆 LED 視覺指示。輸出 `/piezo channel velocity rawPeak` + 連續 stream `/piezo/stream`。同動車三件組之一。詳見 [`piezo_detect/piezo_4drum/README.md`](piezo_detect/piezo_4drum/README.md)。
4-channel piezo strike detection with dynamic baseline, IIR filter, and per-channel LED feedback. One of the 同動車 trio.

### breath_sensor
HX710B 吹氣/吸氣感測 + 超音波霧化器 PWM 控制 + WS2812 LED 動畫（旋轉白點，吹氣指數加速、動態拖尾長度）+ ToF 距離決定底色色溫。最新版本：[`breath_sensor/breath_0115_c3/`](breath_sensor/breath_0115_c3/)（ESP32-C3 SuperMini）。
HX710B breath sensing + ultrasonic mister PWM + WS2812 LED animation (exponential dot acceleration, dynamic tail length) + ToF-driven base color. Latest: `breath_0115_c3/` on ESP32-C3 SuperMini.

### duo_pulse_sonification
雙人脈搏互動系統，同時擷取兩位參與者心跳，透過自動校準三段式演算法（v2.4）偵測 BPM、心跳觸發與手指狀態。附 `heartbeats-harmony.html` 視覺展示：以 p5.js 繪製沙畫李薩如圖形，支援 Web Serial API 直接從 Chrome 讀取 ESP32 資料。
Dual-participant heartbeat system with three-state auto-calibration firmware (v2.4) outputting BPM, beat trigger, and finger detection. Includes `heartbeats-harmony.html` — a p5.js Lissajous sand-drawing demo with Web Serial API support.

### piezo_detect_who
單通道 8kHz 壓電原始波形串流（921600 baud），給 FluCoMa / MuBu / SuperCollider / Max-MSP 做即時特徵抽取（MFCC、頻譜、onset 偵測）。基於 `piezo_detect.ino` 加上 WHO 協定。
Single-channel 8kHz raw piezo waveform stream (921600 baud) for FluCoMa / MuBu / SC / Max real-time feature extraction. Based on `piezo_detect.ino` with WHO protocol added.

### piezo_detect_fft
壓電 FFT 頻譜分析器（I2S ADC 16kHz，1024-point FFT，32 對數頻帶），含 hit（突發打擊）與 scrub（高頻摩擦）事件偵測。
Piezo FFT analyzer (I2S ADC 16kHz, 1024-point FFT, 32 log bands) with hit (transient) and scrub (high-freq friction) event detection.

### local_mediapipe
使用 MediaPipe 在本地端進行手部追蹤，結合 Max/MSP 與網頁視覺化。包含 `2hands_mediapipe.maxpat`（為 LA Life in Motion 演出開發的雙手追蹤）。
Local hand tracking using MediaPipe with Max/MSP and web visualization. Includes `2hands_mediapipe.maxpat` (developed for LA Life in Motion).

### remote_hand_tracking
透過 WebSocket 從遠端機器接收 MediaPipe 手部追蹤資料。
Receives MediaPipe hand tracking data from a remote machine via WebSocket.

### legacy_local_cv_engine
初版的本地影像動態偵測引擎，使用 Python OpenCV 進行動態偵測，由 Max/MSP 的 Node.js 腳本啟動。
Legacy local computer vision engine using Python OpenCV for motion detection, launched from Max/MSP via Node.js.

---

## 授權 | License

MIT License. See [LICENSE](LICENSE) for details.
