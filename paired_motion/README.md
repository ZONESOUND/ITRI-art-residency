# Paired Motion

工研院藝術進駐「**節奏繞纏**」（Rhythmic Entanglements）專案的演出主 patch。

整合三組感測器（Pressure / TOF / Piezo）成一個雙手互動樂器（同動車），以 Max/MSP 即時聲音合成。

> 本資料夾是**演出版本**——zip 起來給合作者就能完整跑、跨電腦移植不需重新設定。
> 設計動機、藝術構想、未來應用見 [主 repo README 的「演出整合：paired_motion 詳細介紹」](../README.md#演出整合paired_motion-詳細介紹--performance-integration-paired_motion-in-detail)。
> 本份文件聚焦在**這個資料夾的內容**：怎麼用、怎麼改、怎麼維護。

---

## 目錄

- [快速開始](#快速開始)
- [資料夾結構](#資料夾結構)
- [系統架構](#系統架構)
- [ESP32 Port 對應](#esp32-port-對應)
- [Abstraction 設計](#abstraction-設計)
- [跟其他資料夾的關係](#跟其他資料夾的關係)
- [演出版本控制](#演出版本控制)
- [待完成 / Roadmap](#待完成--roadmap)

---

## 快速開始

第一次拿到這份資料夾的人（包括未來自己）：

1. 確認 Mac 上裝了 Max/MSP 9 跟 Node.js 16+
2. 三顆 ESP32（Pressure / TOF / Piezo）插到 USB Hub
3. Max 開啟 `paired_motion.maxproj`
4. 雙擊 `patchers/main.maxpat`
5. **第一次跑**（`code/node_modules/` 不存在）：點 patch 上的「npm install」按鈕，console 會印 `npm success dictionary ...`
6. 裝完後送 `script restart` 給 [node.script]（或重新載入 patch），讓 auto_detect.js 重新載入
7. console 應顯示「掃描結果」三組 ID 都被找到 → 開始演出

之後每次開只要 1~2 秒（node_modules 已存在，跳過 npm install）。

> 不需要開 Terminal、不需要手動 `npm install`，在 Max patch 裡按按鈕就完成。

---

## 資料夾結構

```
paired_motion/
├── paired_motion.maxproj            ← Max Project 檔（autoorganize=0）
├── README.md                         ← 你正在看
├── openactions.txt                   ← Max 自動產生的 project 開啟動作
│
├── patchers/                         ← 所有 .maxpat（Max 慣例位置）
│   ├── main.maxpat                   ← 演出主 patch
│   ├── sub_auto_detect.maxpat        ← auto-detect + 三 [serial] + 解析鏈
│   ├── sub_tof.maxpat                ← TOF 訊號處理
│   ├── sub_pressure.maxpat           ← Pressure 訊號處理
│   ├── sub_piezo.maxpat              ← Piezo 訊號處理
│   ├── p_resonators~.maxpat          ← Cycling74 abstractions（consolidate 拉進來）
│   ├── p_resontaps~.maxpat
│   └── vs.*.maxpat                   ← Cycling74 vs.* 系列工具
│
├── code/                             ← Node.js 自動化
│   ├── auto_detect.js                ← USB port 自動掃描 + WHO 識別（patch 載入時跑）
│   ├── who_probe.js                  ← 命令列單 port 診斷工具（debug 用，不在 patch 內）
│   ├── package.json                  ← 依賴宣告（serialport ^12）
│   ├── package-lock.json
│   └── node_modules/                 ← npm install 後產生（git 不追）
│
├── media/                            ← 取樣（consolidate 拉進來）
│   ├── Bubbles_ Big_ Fast_ Gurgling Up.aif
│   ├── EQ-Lp011 Ejects Rhythm 065.wav
│   ├── EQ-Lp013 Express Rhythm 065.wav
│   └── Heavy Cold Gusts Howling.aif
│
├── externals/                        ← 編譯過的 .mxo（PeRColate physical modeling）
│   ├── bowedbar~.mxo/
│   └── bowed~.mxo/
│
└── presets/                          ← 演出參數 snapshot
    └── 20yymmdd_場地名.maxsnap
```

> Consolidate 過後所有引用的取樣、Cycling74 abstractions、PeRColate externals 都被複製進此資料夾。**對方不需要單獨安裝 vs library 或 PeRColate package**，patch 也照樣跑。

---

## 系統架構

```
硬體層 / Hardware
  ┌───────────────────────────────────────────┐
  │  ESP32-C3 #1     ESP32-C3 #2    ESP32-C3 #3
  │  (Pressure)      (TOF)          (Piezo 4-drum)
  │   │ FSR x2        │ VL53L0X x2   │ Piezo x4 + LED x4
  │   │ LED ring x2   │ Button+LED   │
  │   └────── USB Hub ──────────────┘
  └────────────┬──────────────────────────────┘
               │
               ▼
Mac 端 / Max + Node.js
  ┌───────────────────────────────────────────┐
  │  paired_motion.maxproj
  │       ↓
  │  patchers/main.maxpat
  │       │
  │       ├── [bpatcher sub_auto_detect.maxpat]
  │       │     ├── [node.script ../code/auto_detect.js]
  │       │     │      ↓ (掃描三 port + WHO 握手)
  │       │     ├── [serial a/b/c 115200 8 1] x 3
  │       │     │      ↓ (依韌體前綴 route 分流)
  │       │     └── outlet: /tof  /pressure  /piezo  /piezo/stream
  │       │
  │       ├── [bpatcher sub_tof.maxpat]      → 聲響映射
  │       ├── [bpatcher sub_pressure.maxpat] → 聲響映射
  │       ├── [bpatcher sub_piezo.maxpat]    → 聲響映射
  │       │
  │       └── [混音 + dac~] → 喇叭
  └───────────────────────────────────────────┘
```

每個 `sub_*` 負責**一種感測器的訊號處理 + 聲響映射**，主 patch 只做佈線、混音、輸出。

---

## ESP32 Port 對應

每顆 ESP32 的 USB port 名（短名）由 USB 序號決定，**不會因為換 USB 孔變動**：

| 末 4 碼 | 裝置 | ESP32 上實際燒的韌體 |
|---|---|---|
| `1423101` | Pressure | `pressure_sensor/pressure_2hands/pressure_2hands.ino` |
| `1423301` | TOF | `tof_distance_sensor/tof_c3_supermini_vel_norm/tof_c3_supermini_vel_norm.ino`（8 值版）|
| `1423401` | Piezo | `piezo_detect/piezo_4drum/piezo_4drum.ino` |

所有 ESP32 韌體都實作 WHO 識別協定——auto_detect.js 對每顆送 `WHO\n`，根據回應的 `ID:tof` / `ID:pressure` / `ID:piezo` 配對 port 名給 Max 的 `[serial]` 物件。

WHO 機制細節見 [`../serial_auto_detect/README.md`](../serial_auto_detect/README.md)。

---

## Abstraction 設計

每個感測器一個 abstraction，獨立處理訊號、做 normalize / mapping，輸出乾淨的訊號給 main.maxpat 接到聲音模組。

### sub_auto_detect

**位置**：`patchers/sub_auto_detect.maxpat`

**功能**：USB port 自動掃描 + 三組 `[serial]` 開啟 + 行解析（sel 10 13 → zl group → itoa → fromsymbol）+ 內容路由（route /tof /pressure /piezo /piezo/stream）

**Inlet**：（無——內部由 [node.script ../code/auto_detect.js] 的 outlet 驅動）

**Outlet**：

| 編號 | 訊息來源 | 內容（list） |
|---|---|---|
| 1 | `/tof` | `fX fY rX rY vX vY vXn vYn`（**8 個 atom**，TOF 韌體 `_vel_norm` 版輸出）|
| 2 | `/pressure` | `norm1 norm2 raw1 raw2`（4 個 atom） |
| 3 | `/piezo` | `channel velocity rawPeak`（3 個 atom，敲擊事件，偶發） |
| 4 | `/piezo/stream` | `d1 d2 d3 d4`（4 個 atom，50Hz 連續） |

> 也可以再加 outlet 接 `/status`、`/error` 給 dashboard 顯示連線狀態。

### sub_tof

**位置**：`patchers/sub_tof.maxpat`

**Inlet**：sub_auto_detect 的 `/tof` outlet（list of **8**）

**內部解包**：

```
inlet  ──→  [unpack i i i i f f f f]
              │  │  │  │  │  │  │   │
              fX fY rX rY vX vY vXn vYn
```

| 變數 | 型別 | 範圍 | 處理層級 | 用途 |
|---|---|---|---|---|
| fX, fY | int | 0 ~ 2000 mm | 三層濾波（Median + 自適應 EMA + Deadband）| 穩定位置 |
| rX, rY | int | 0 ~ 2000 mm | 只校正 offset，無平滑 | 原始訊號（debug） |
| vX, vY | float | 典型 ±50~500 mm/s | EMA + 位置不變 snap-to-0 | 絕對速度 |
| **vXn, vYn** | float | **-1.0 ~ +1.0** | 韌體已 normalize + deadband | **直接接聲音映射** |

**重點：vXn / vYn 已經是 -1~1，不需要再 normalize**。

韌體端 commit `f68ade6` 起的「位置不變 snap-to-0」 + `tof_c3_supermini_vel_norm` 版的 normalize（除以 VEL_MAX=500、clip ±1.0、deadband 0.02）保證 vXn 在靜止時就是 0.0（exact）。

**建議的 outlet 配置**：

| outlet | 名稱 | 範圍 | 公式 |
|---|---|---|---|
| 1 | fX | 0 ~ 2000 mm | 直通 |
| 2 | fY | 0 ~ 2000 mm | 直通 |
| 3 | fX_norm | 0.0 ~ 1.0 | `fX / 2000.` 後 clip |
| 4 | fY_norm | 0.0 ~ 1.0 | 同上 |
| 5 | **vXn** | -1.0 ~ +1.0 | 直通（韌體已處理） |
| 6 | **vYn** | -1.0 ~ +1.0 | 直通 |

下游需要絕對值（接 amplitude / filter）自己加 `[abs]`，需要方向（接 pan / pitch）直接吃 vXn / vYn。

**演出當下想調 normalize 上限**：要重燒韌體（修 `_vel_norm` 裡的 `VEL_MAX`）。Max 端為了一致性不再做 fallback normalize。

韌體層細節見 [`../tof_distance_sensor/README.md`](../tof_distance_sensor/README.md)。

### sub_pressure

**位置**：`patchers/sub_pressure.maxpat`

**Inlet**：sub_auto_detect 的 `/pressure` outlet（list of 4）

**內部處理**：

```
inlet  ──→  [unpack f f i i]
              │  │  │  │
            norm1 norm2 raw1 raw2
```

| 變數 | 型別 | 範圍 | 用途 |
|---|---|---|---|
| norm1, norm2 | float | 0.0 ~ 1.0 | 已 normalize 的握力強度（左/右手）|
| raw1, raw2 | int | 0 ~ 4095 | 原始 ADC 值（debug、診斷）|

**設計重點**：

- norm 已是 0~1 範圍，**不需要再 normalize**
- 韌體會自動校正（10 秒）+ 動態擴展上限（壓超過校正值會自動更新）
- 閒置 10 秒會進入 idle 模式（norm 強制歸 0）
- 雙手獨立成兩條訊號鏈——根據 Paul 在淡水義山日照中心的工作坊觀察，長者使用同動車時傾向雙手同步用力，缺乏左右手分離控制，本模組設計上特別把兩手獨立

**建議的 outlet 配置**（待 user 決定）：

| outlet | 名稱 | 範圍 | 用途 |
|---|---|---|---|
| 1 | norm1 (左手) | 0.0 ~ 1.0 | 直接接 amplitude / filter |
| 2 | norm2 (右手) | 0.0 ~ 1.0 | 同上 |
| 3 | norm_sum | 0.0 ~ 2.0 | 雙手合計力道 |
| 4 | norm_diff | -1.0 ~ +1.0 | 左右差（適合 panning） |

韌體層細節見 [`../pressure_sensor/README.md`](../pressure_sensor/README.md)。

### sub_piezo

**位置**：`patchers/sub_piezo.maxpat`

**Inlets**：

- inlet 1：sub_auto_detect 的 `/piezo` outlet（list of 3，敲擊事件）
- inlet 2：sub_auto_detect 的 `/piezo/stream` outlet（list of 4，50Hz 連續）

**內部處理**：

敲擊事件：
```
inlet 1 ──→ [unpack i i i] ──→ channel(1~4) velocity(1~127) rawPeak(0~4095)
                                  │
                            [route 1 2 3 4]   ← 依通道分流
                            ↓ ↓ ↓ ↓
                          ch1 ch2 ch3 ch4 各自的觸發訊號
```

連續活動：
```
inlet 2 ──→ [unpack i i i i] ──→ d1 d2 d3 d4（每通道活動量，≥0）
                                  │
                            [/ 2000.] x 4    ← normalize 用 2000（重擊上限）
                                  │
                            [clip 0. 1.] x 4
                                  │
                          ch1_act ch2_act ch3_act ch4_act
```

**設計分工**：

- 敲（hit event）：觸發離散音件（鼓擊、Tiny Sound 合成）
- 刮 / 摸 / 持續按壓（continuous stream）：連續控制（filter cutoff、reverb send、音色切換）
- 同一塊壓電片，敲出鼓打點、刮出連續音色變化

**建議的 outlet 配置**（待 user 決定）：

| outlet | 名稱 | 內容 | 用途 |
|---|---|---|---|
| 1 | ch1_hit | velocity (1~127) | 通道 1 敲擊力度 |
| 2 | ch2_hit | velocity (1~127) | 通道 2 |
| 3 | ch3_hit | velocity (1~127) | 通道 3 |
| 4 | ch4_hit | velocity (1~127) | 通道 4 |
| 5 | ch1_activity | 0.0 ~ 1.0 | 通道 1 連續活動量 |
| 6 | ch2_activity | 0.0 ~ 1.0 | 通道 2 |
| 7 | ch3_activity | 0.0 ~ 1.0 | 通道 3 |
| 8 | ch4_activity | 0.0 ~ 1.0 | 通道 4 |

韌體層細節見 [`../piezo_detect/README.md`](../piezo_detect/README.md) 與 [`../piezo_detect/piezo_4drum/README.md`](../piezo_detect/piezo_4drum/README.md)。

---

## 跟其他資料夾的關係

| 資料夾 | 角色 |
|---|---|
| `paired_motion/`（本資料夾） | **演出版本** —— 凍結在已知可用狀態，給合作者用 |
| [`../serial_auto_detect/`](../serial_auto_detect/) | **實驗室** —— 開發 / debug auto-detect 機制 |
| [`../pressure_sensor/`](../pressure_sensor/) | Pressure ESP32 韌體（含 README） |
| [`../tof_distance_sensor/`](../tof_distance_sensor/) | TOF ESP32 韌體（含 README） |
| [`../piezo_detect/`](../piezo_detect/) | Piezo ESP32 韌體（含 README） |

### `code/auto_detect.js` 跟 `serial_auto_detect/auto_detect.js` 的關係

**這兩個是獨立的檔案，內容相同但分開維護。**

Max patch 載入時讀的是**自己資料夾裡** `paired_motion/code/auto_detect.js`，跟 `serial_auto_detect/auto_detect.js` 沒有任何即時連動。它們會「相同」只是因為**最初是用 `cp` 從 serial_auto_detect 複製過來**——之後各自演化，不會自動同步。

| | serial_auto_detect/auto_detect.js | paired_motion/code/auto_detect.js |
|---|---|---|
| 角色 | 實驗版（debug、改 timeout、加新功能） | 演出版（已驗證可用，不亂動） |
| 誰會用 | 開發時用 `auto_detect_test.maxpat` 測 | paired_motion 的 Max patch 載入 |
| 改動頻率 | 高（一直迭代） | 低（演出前才會改） |

這樣分的目的：**實驗版改壞不會炸到演出版**。在 serial_auto_detect 那邊試新東西、debug 完了，**手動**用一行 `cp` 把成果複製進演出版，commit + tag 為某場演出的還原點：

```bash
# 從實驗版手動同步到演出版
cp ../serial_auto_detect/auto_detect.js code/auto_detect.js

# 確認沒問題後 commit + 標 tag
git commit -m "sync(paired_motion): pull latest auto_detect.js from dev"
git tag 演出_yymmdd_場地名
git push origin --tags
```

**沒手動 `cp` 的話，paired_motion 永遠跑它自己的舊版**——這是設計上的安全網，不是 bug。

---

## 演出版本控制

每場演出前 commit + git tag 標記：

```bash
git tag 演出_20260617_文化部訪視
git push origin --tags
```

之後想還原任何一場版本：

```bash
git checkout 演出_20260617_文化部訪視
```

`presets/` 裡的 maxsnap 檔對應每場演出當下調好的參數，跟 git tag 配對使用。

### 已知還原點

| Tag | 內容 |
|---|---|
| `paired_motion_skeleton` | 骨架完成（資料夾、Project、依賴複製、placeholder patch） |
| `tof_normalized_firmware` | TOF 韌體升級到 8 值 normalize 版本 |

---

## 待完成 / Roadmap

### 已完成

- [x] sub_auto_detect.maxpat —— auto-detect 邏輯封裝
- [x] sub_tof.maxpat —— 訊號處理（韌體已輸出 normalized 速度，sub_tof 直接 unpack）
- [x] sub_pressure.maxpat —— 訊號處理
- [x] sub_piezo.maxpat —— 訊號處理（敲擊事件 + 連續活動兩種輸出）
- [x] 取樣素材 consolidate 進 `media/`
- [x] Cycling74 abstractions + PeRColate externals consolidate 進 project

### 待完成

- [ ] `main.maxpat` 內 bpatcher 連接完成
- [ ] 各 abstraction 串到聲音模組（依現有 `media/` 取樣設計聲響）
- [ ] 主混音 + dac~ 輸出
- [ ] `presets/default.maxsnap` 預設參數
- [ ] 演出實機跑過完整流程，commit + tag 第一個演出版本
- [ ] 演出前測試文檔（換筆電、換 hub、現場可能突發狀況的處理流程）
