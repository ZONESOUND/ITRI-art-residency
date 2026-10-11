# ITRI Art Residency — Interactive Sensing Modules

工研院藝術進駐「**節奏繞纏**」（*Rhythmic Entanglements: Sonification Experiments on Biofeedback and Embodied Perception*）專案的程式碼、韌體、演出檔與聲音工具。

「**同動車**」是富伯生醫（Rehabotics）開發的**中風上肢復健輔具**，採用「好手帶壞手」連動機制：患者用健側手帶動機構，讓患側手隨動，協助動作復健；工研院音樂與動作互動健促實驗室在裝置上加入動作追蹤與數據紀錄。本專案在駐村期間與該實驗室合作，**在同動車上加裝 Pressure（壓力）／ToF（距離）／Piezo（壓電）三組感測器**，把使用者操作時的力道、移動、敲擊轉成即時聲響。

「同動車」(literally "synchronous-motion vehicle") is a stroke rehabilitation device developed by Rehabotics (富伯生醫) using the well-hand-leads-affected-hand bimanual mechanism; ITRI's Music and Motion Interactive Health Promotion Lab added motion tracking and data logging to it. This residency project instruments the device with three sensors (pressure / ToF / piezo) and maps user interaction into real-time sound synthesis.

---

## 要做什麼，開哪裡 | Where to Start

| 我要… | 開這個 |
|---|---|
| 跑演出的互動聲音（Max） | [`paired_motion/paired_motion.maxproj`](paired_motion/) → `patchers/main.maxpat` |
| 跑演出的配樂與場景（Ableton Live） | [`live_demo/Live_Demo Project/ITRI_show_MIDI.als`](live_demo/)（10/9 排練後最新版）或 `ITRI_show.als` |
| 燒錄或修改感測器韌體 | [`pressure_sensor/`](pressure_sensor/)、[`tof_distance_sensor/`](tof_distance_sensor/)、[`piezo_detect/`](piezo_detect/) |
| 感測器連不上、port 認錯 | [`serial_auto_detect/`](serial_auto_detect/) 的 `who_probe.js` 與 README 排查流程 |
| 離線處理聲音素材（varispeed、磁帶效果、stems 回對） | [`sound_tools/`](sound_tools/)：`uv sync` 後 `uv run soundtools --help` |
| 接一顆新的 Arduino 感測器 | [`arduino_template.maxpat`](arduino_template.maxpat) |

---

## 檔案結構 | Repository Structure

只列主要檔案；各資料夾的完整說明見該夾 README。

```
ITRI-art-residency/
├── README.md                      ← 本檔
├── CLAUDE.md                      ← 給 Claude Code 的架構與操作說明（英文）
├── LICENSE                        ← MIT
├── .gitattributes                 ← live_demo/ 底下的音檔走 Git LFS
├── arduino_template.maxpat        ← 通用 Arduino-over-Serial 接收範本
│
├── paired_motion/                 ← ★ 演出主程式（Max Project，自包含，可整包帶走）
│   ├── paired_motion.maxproj      ← 用 Max 9 開這個
│   ├── patchers/
│   │   ├── main.maxpat            ← 主 patch：接線、混音、輸出
│   │   ├── main_viz.maxpat        ← main 的副本，多一組 ToF 軌跡視覺化
│   │   ├── sub_auto_detect.maxpat ← 自動配對三顆 ESP32 的 serial port
│   │   ├── sub_pressure / sub_tof / sub_piezo.maxpat ← 三組感測器各自的訊號→聲音映射
│   │   ├── sub_direction / sub_voice_gate / p_resonators~ / p_resontaps~ ← 方向判斷、人聲觸發、共鳴器
│   │   └── vs.*.maxpat            ← Cycling '74 vs library 的 abstractions
│   ├── code/                      ← auto_detect.js、who_probe.js（serial_auto_detect 的凍結副本）
│   ├── externals/                 ← PeRColate 的 bowed~、bowedbar~
│   ├── media/                     ← 互動觸發的音檔（小孩聲音、風聲、氣泡、節奏 loop）
│   ├── data/、presets/            ← 裝置快照與演出版本的 preset
│   ├── visualization/             ← ToF 軌跡網頁視覺化（Node SSE server，localhost:8080）
│   └── 檔案導覽.md
│
├── live_demo/                     ← ★ Ableton Live 演出專案（與 paired_motion 各自獨立開）
│   └── Live_Demo Project/
│       ├── ITRI_show_MIDI.als     ← 演出 set，10/9 排練後版本（調整 MIDI 對應與參數）
│       ├── ITRI_show.als          ← 演出 set，10/7 排練調整後的版本
│       ├── Live_Demo.als          ← 早期 demo set
│       ├── Live_Demo_macstudio.als← demo set 的 Mac Studio 版
│       ├── SceneBridge.amxd       ← M4L：從 UDP 7400 收整數 N，觸發 Live 第 N 個 scene
│       ├── autoStart.amxd         ← M4L：載入後讓 Live 開始播放
│       ├── recording_bell.wav、recording_bell_C.wav、recording_melody.wav、Night animals.wav ← 配樂素材（LFS）
│       ├── Samples/               ← Collect All and Save 收進來的音檔（LFS）
│       └── Presets/、Ableton Project Info/
│
├── pressure_sensor/               ← 韌體：雙手 FSR 握力＋WS2812 燈圈（WHO ID: pressure）
├── tof_distance_sensor/           ← 韌體：雙 VL53L0X 把手 X/Y 位置與速度（WHO ID: tof）
├── piezo_detect/                  ← 韌體：4 通道壓電，敲擊事件＋連續活動（WHO ID: piezo）
├── serial_auto_detect/            ← Node.js：USB port 掃描＋WHO 握手＋診斷工具
│
├── sound_tools/                   ← Python 套件 soundtools＋指令列（uv 管理）
│   ├── soundtools/                ← varispeed、磁帶效果、paulstretch、樂句與音節切分、stems 回對
│   └── tape_drift/                ← 同一套 varispeed 演算法的網頁版與 gen~ 版
│
└── 開發歷程中的其他模組（未整合進演出版）
    ├── breath_sensor/             ← 吹氣樂器：HX710B＋超音波霧化器＋燈圈
    ├── duo_pulse_sonification/    ← 雙人脈搏聲音化（p5.js Lissajous＋Web Serial，含 ws_osc_relay）
    ├── piezo_detect_fft/          ← 壓電 FFT 頻譜分析（hit／scrub）
    ├── local_mediapipe/           ← 本地 MediaPipe 手部追蹤（LA Life in Motion 演出用）
    ├── remote_hand_tracking/      ← 經 WebSocket 接收遠端手部追蹤資料
    └── legacy_local_cv_engine/    ← 早期 Python OpenCV 動態偵測（已被 local_mediapipe 取代）
```

---

## 各資料夾的功能與用途 | Folders

### 演出用 | Performance

| 資料夾 | 功能 | 用途 |
|---|---|---|
| **[`paired_motion/`](paired_motion/)** | Max 演出主程式。三組感測器各有一個 `sub_*.maxpat` 做訊號整理與聲音映射，`main.maxpat` 只負責接線、混音、輸出 | 演出時的即時互動聲音。整個資料夾 zip 帶到別台 Mac 就能跑 |
| **[`live_demo/`](live_demo/)** | Ableton Live 專案：配樂、場景、M4L 裝置。`SceneBridge.amxd` 讓外部 Max patch 經 UDP 7400 切換 Live 的 scene | 演出時的配樂與段落切換。與 `paired_motion/` 分開開、分開存 |

### 同動車三件感測器 | The Sensor Trio

接同一個 USB Hub，全部使用 ESP32-C3 SuperMini、115200 baud，都支援 WHO 裝置識別協定。

| 資料夾 | 功能 | WHO ID | 訊號 |
|---|---|---|---|
| [`pressure_sensor/`](pressure_sensor/) | 雙手 FSR 握力＋WS2812 燈圈視覺回饋，左右手各自一條訊號鏈 | `pressure` | 0.0–1.0 浮點，左右獨立 |
| [`tof_distance_sensor/`](tof_distance_sensor/) | 雙 VL53L0X 追蹤把手 X/Y 位置與速度 | `tof` | 距離 mm＋正規化速度 −1～1 |
| [`piezo_detect/`](piezo_detect/) | 4 顆壓電片：敲擊觸發離散事件，刮、摸、持續按壓輸出連續活動量 | `piezo` | velocity 1–127＋0–1 連續強度 |

### 支援工具 | Supporting Tools

| 資料夾 | 功能 | 用途 |
|---|---|---|
| [`serial_auto_detect/`](serial_auto_detect/) | 掃描 `cu.usbmodem*`、發 WHO 握手、把正確 port 名餵給 Max `[serial]`；`who_probe.js` 是命令列診斷工具 | 解決 USB 插拔後 port 順序會變的問題。`paired_motion/code/` 是它的凍結副本，刻意不自動同步 |
| [`sound_tools/`](sound_tools/) | Python 套件 `soundtools`：varispeed 多聲部漂移與重同步、磁帶效果、paulstretch、樂句邊界、音節切分、stems 回對原檔；另附 Tape Drift 網頁版與 `gen~` 版 | 2026 年 8 到 10 月處理小星星與注音素材時寫的離線工具，之後可跨專案使用 |
| [`arduino_template.maxpat`](arduino_template.maxpat) | 與具體感測器無關的 Arduino-over-Serial 接收範本 | 新接一顆 Arduino 時從這裡改起 |

### 開發歷程中的其他模組 | Phased Development Outputs

駐村期間不同階段的探索與獨立子專案，**未必整合進演出版**，但各自完成過演出、工作坊或技術探索，保留作為日後迭代的素材。各夾自帶 README。

| 資料夾 | 功能 |
|---|---|
| [`breath_sensor/`](breath_sensor/) | 吹氣樂器：HX710B＋超音波霧化器＋WS2812 燈圈動畫 |
| [`duo_pulse_sonification/`](duo_pulse_sonification/) | 雙人脈搏聲音化（p5.js Lissajous＋Web Serial API），含 `ws_osc_relay/` WebSocket→OSC 橋接 |
| [`piezo_detect_fft/`](piezo_detect_fft/) | 壓電 FFT 頻譜分析（hit／scrub 事件偵測） |
| [`local_mediapipe/`](local_mediapipe/) | 本地 MediaPipe 手部追蹤（為 LA Life in Motion 演出開發） |
| [`remote_hand_tracking/`](remote_hand_tracking/) | 經 WebSocket 從遠端機器接收手部追蹤資料，附同動車 API 簡易使用說明 PDF |
| [`legacy_local_cv_engine/`](legacy_local_cv_engine/) | 早期 Python OpenCV 動態偵測引擎（已被 local_mediapipe 取代） |

---

## 演出時的資料流 | Performance Data Flow

```
3× ESP32-C3 → USB hub → Mac
  paired_motion/patchers/main.maxpat
    ├ sub_auto_detect.maxpat   ← node.script 掃 port＋WHO 握手，三個 [serial] 以 50Hz 讀取
    ├ sub_tof / sub_pressure / sub_piezo.maxpat ← 各感測器的訊號→聲音映射
    └ 混音 → dac~ → 喇叭
  （需要時）Max → UDP 7400 → live_demo 的 SceneBridge.amxd → 觸發 Live 的 scene
```

韌體端已經做好正規化（ToF 速度 −1～1、Pressure 0–1），Max 端不再重複正規化。

---

## WHO 裝置識別協定 | WHO Identification Protocol

三件感測器接同一個 USB Hub 時，macOS 配發的 port 編號會隨插入順序與 USB 孔改變，無法靠順序辨識。三組韌體都實作了 WHO 協定：

```
電腦端 → 對每個 cu.usbmodem* 發送 "WHO\n"
ESP32 → 回覆 "ID:pressure" / "ID:tof" / "ID:piezo"
```

自動化工具與完整排查流程見 [`serial_auto_detect/`](serial_auto_detect/)。

When the trio shares a USB hub, port enumeration order is unstable across replug. All three firmwares implement WHO so the host can identify each device deterministically.

---

## 開發環境 | Development Setup

**Mac 端：**
- Max/MSP 9、Ableton Live 12 Suite
- Node.js 16+（給 Max `[node.script]` 用，`serialport` 等套件）：各 Node 資料夾分別 `npm install`（`paired_motion/code/`、`serial_auto_detect/`）
- Python 3＋[uv](https://docs.astral.sh/uv/)（`sound_tools/`）
- Git LFS（`live_demo/` 的音檔）：clone 後跑 `git lfs install && git lfs pull`

**Arduino：**
- Board 選 `ESP32C3 Dev Module`，USB CDC On Boot 設 **`Enabled`**（三件都需要，否則 Serial 走錯通道）
- 函式庫：`Adafruit_VL53L0X`、`Adafruit_NeoPixel`
- 命令列燒錄：`arduino-cli upload -p /dev/cu.usbmodemXXXX --fqbn esp32:esp32:esp32c3:CDCOnBoot=cdc <sketch_dir>`（先關 Max 釋放 port）

**通訊：** USB Serial 115200 baud，OSC 風格訊息前綴（`/tof`、`/pressure`、`/piezo`），Max 端用 `[route]` 分流。

---

## 版本標記 | Version Tags

排練、演出、展覽可以各自標一個版本，搭配 `paired_motion/presets/` 的快照：

```
git tag 排練-YYYYMMDD
git tag 演出-YYYYMMDD
git tag 展覽-YYYYMMDD
git push origin --tags
```

用 `git checkout <tag>` 回到任一個版本。

---

## 授權 | License

MIT License，詳見 [LICENSE](LICENSE)。
