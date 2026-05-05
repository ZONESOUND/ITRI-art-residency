# VL53L0X 雙 ToF 距離感測模組

ESP32 + 2x VL53L0X ToF（Time-of-Flight）感測器，用於平面同動車 X/Y 軸手把追蹤。
Serial 輸出 OSC 風格格式，可直接接入 Max/MSP。

---

## 韌體版本

本模組包含三個韌體版本，依開發順序排列：

| 目錄 | 板子 | 濾波 | 輸出格式 | 說明 |
|------|------|------|----------|------|
| `tof_noSmooth/` | ESP32 Dev Module | 無 | `x=N,Y=M` | 最早版本，原始距離直出 |
| `tof_optimized/` | ESP32 Dev Module | Median + 自適應 EMA | `/tof fX fY rX rY` | 優化版，雙層濾波 |
| `tof_c3_supermini/` | ESP32-C3 SuperMini | Median + 自適應 EMA + Deadband | `/tof fX fY rX rY` | 三層濾波，僅位置 |
| **`tof_c3_supermini_vel/`** | **ESP32-C3 SuperMini** | **同上 + 速度 ramp** | **`/tof fX fY rX rY vX vY`** | **位置 + 速度版本** |

> `tof_c3_supermini` 和 `tof_c3_supermini_vel` 的前四個值格式相同。
> 舊的 Max patch（`[unpack i i i i]`）可以直接用 `_vel` 版本，只是忽略速度。
> 要接收速度改用 `[unpack i i i i f f]`。

---

## 硬體接線

### ESP32-C3 SuperMini（目前使用）

```
ESP32-C3 SuperMini    VL53L0X #1 (X軸)    VL53L0X #2 (Y軸)
──────────────────    ────────────────    ────────────────
GPIO 5 (SDA) ──────── SDA ──────────── SDA
GPIO 6 (SCL) ──────── SCL ──────────── SCL
3.3V ─────────────── VIN ──────────── VIN
GND ──────────────── GND ──────────── GND
GPIO 4 ──────────── XSHUT
GPIO 3 ─────────────────────────────── XSHUT
GPIO 0 ──────────── 外接按鈕（另一端接 GND，按下重新校正）
GPIO 8 ──────────── 狀態 LED（校正中閃爍，運行中常滅）
```

### ESP32 Dev Module（舊版）

```
ESP32                 VL53L0X #1 (X軸)    VL53L0X #2 (Y軸)
─────                 ────────────────    ────────────────
GPIO 21 (SDA) ──────── SDA ──────────── SDA
GPIO 22 (SCL) ──────── SCL ──────────── SCL
3.3V ─────────────── VIN ──────────── VIN
GND ──────────────── GND ──────────── GND
GPIO 25 ──────────── XSHUT
GPIO 26 ─────────────────────────────── XSHUT
```

> 兩顆感測器共用 I2C 匯流排，透過 XSHUT 腳位依序啟動並重新分配地址（0x30, 0x31）。
> VL53L0X 只能接 3.3V，不可接 5V。

---

## 安裝與燒錄

### 安裝依賴

在 Arduino IDE 中安裝：

1. **Library Manager** → 搜尋 `Adafruit VL53L0X` → 安裝（會自動安裝 `Adafruit BusIO` 等依賴）

### Board 設定

**ESP32-C3 SuperMini（`tof_c3_supermini`）：**

| 設定項目 | 值 |
|----------|-----|
| Board | ESP32C3 Dev Module |
| USB CDC On Boot | **Enabled**（必須，否則 Serial Monitor 無輸出） |
| Partition Scheme | Default 4MB with spiffs |

**ESP32 Dev Module（`tof_optimized` / `tof_noSmooth`）：**

| 設定項目 | 值 |
|----------|-----|
| Board | ESP32 Dev Module |

---

## 運作流程

上電後自動進入三階段狀態機：

```
┌─────────┐     500ms     ┌──────────────┐     5 秒      ┌─────────┐
│  暖機   │ ────────────→ │    校正      │ ────────────→ │  運行   │
│ WARMUP  │  丟棄不穩讀數  │ CALIBRATING  │  收集中位數    │ RUNNING │
└─────────┘               └──────────────┘               └─────────┘
```

### 校正

1. **暖機（500ms）**：丟棄開機後不穩定的讀數
2. **校正（5 秒）**：收集有效樣本，取**中位數**作為零點 offset
   - 校正期間請將手把放在**原點位置**不動
   - 中位數比最小值更抗雜訊
3. **運行**：開始輸出濾波後的距離值

### 重新校正

兩種方式：

1. **按鈕**（`_vel` 版）：按下外接按鈕（GPIO0）→ 重新校正，Serial 不中斷，Max 不需重連
2. **Serial 指令**：發送字元 `c` → 重新校正

校正期間 GPIO8 LED 閃爍（500ms 間隔），校正完成後 LED 熄滅。

---

## 三層濾波機制（`tof_c3_supermini`）

```
感測器原始讀值 → 歸零(減 offset) → ① Median → ② 自適應 EMA → ③ Deadband → 輸出
```

### ① Median 濾波（殺突波）

- 窗口大小 = 3，對最近 3 筆取中位數
- 感測器偶爾跳一下（如 120→250→120），中位數會直接忽略 250 這個離群值
- 比 EMA 更適合處理突波，因為 EMA 會被拉走好幾幀

### ② 自適應 EMA（靜止穩、移動快）

- 計算新值與目前 EMA 的差距，自動切換平滑係數：
  - 差距 ≤ 10mm（靜止/緩動）→ alpha = 0.12（新值只佔 12%，非常平滑）
  - 差距 > 10mm（快速移動）→ alpha = 0.6（新值佔 60%，快速跟手）
- 比固定 alpha 好在：靜止時不抖、移動時不拖

### ③ Deadband（鎖住微抖）

- 濾波後的值與上次輸出相差 ≤ 3mm → 不更新，鎖住上次的值
- 確保靜止時輸出完全不動

---

## Serial 輸出格式

Baud rate: **115200**

### 訊息格式（OSC 風格）

| 訊息 | 說明 |
|------|------|
| `/tof <fX> <fY> <rX> <rY>` | 正常量測—僅位置（50Hz） |
| `/tof <fX> <fY> <rX> <rY> <vX> <vY>` | 正常量測—位置 + 速度（`_vel` 版，50Hz） |
| `/status calibrating <seconds_remaining>` | 校正倒數中 |
| `/cal_done <offsetX> <offsetY> <samplesX> <samplesY>` | 校正完成 |
| `/status running` | 開始正常運行 |
| `/status velocity_on` / `velocity_off` | 速度輸出開關切換（`_vel` 版） |
| `/status button_recalibrate` | 按鈕觸發重新校正（`_vel` 版） |
| `/status recalibrating` | 重新進入校正流程（`_vel` 版） |
| `/status filters_reset` | 濾波器已重置 |
| `/error <message>` | 錯誤訊息 |

### `/tof` 數值說明

```
/tof <fX> <fY> <rX> <rY> <vX> <vY>
      ↑         ↑         ↑
      濾波後     僅歸零     速度（_vel 版才有）
```

| | filtered (fX, fY) | raw (rX, rY) | velocity (vX, vY) |
|---|---|---|---|
| 型態 | int (mm) | int (mm) | float (mm/s) |
| 歸零 | 有 | 有 | — |
| Median + EMA + Deadband | 有 | 無 | — |
| 速度 ramp 平滑 | — | — | 有 |
| 用途 | **控制用** | **除錯用** | **動態控制用** |

#### 速度 (vX, vY) 特性

- 單位：**mm/s**，帶正負方向
  - 正值 = 遠離感測器（向中線移動）
  - 負值 = 靠近感測器（向邊緣移動）
- 從 fX/fY（deadband 後穩定值）計算
- **位置沒變就直接 = 0**，速度沒有慣性尾巴（不會在停下後緩慢衰減）
- 移動中才套 EMA 平滑（VEL_SMOOTH = 0.06）→ 加速時連續 ramp，不跳動
- 典型範圍：慢 ±50, 中 ±200, 快 ±500~1000

### Serial 指令

| 指令 | 功能 | 版本 |
|------|------|------|
| `c` | 重新校正（暖機 + 5 秒收集） | 全版本 |
| `r` | 重啟濾波器（清除歷史，保留 offset） | 全版本 |
| `v` | 切換速度輸出開/關（預設開） | `_vel` 版 |

---

## Max/MSP 接線

### 基本接收鏈

```
[serial /dev/cu.usbmodem-XXXX 115200]    ← ESP32-C3 用 usbmodem，ESP32 用 usbserial
        |
    [sel 10]          ← 以換行符號 (ASCII 10) 分割訊息
        |
   [zl group]         ← 收集一行的 bytes
        |
     [itoa]           ← bytes → 字元
        |
   [fromsymbol]       ← 字串 → Max symbol list
        |
  [route /tof /status /cal_done /error]
     |      |         |          |
[unpack i i i i]    ...        ...
  |   |   |   |
 fX  fY  rX  rY
```

### 分離 filtered、raw、velocity

```
[route /tof]
     |
[unpack 0 0 0 0 0. 0.]       ← 最後兩個用 0.（float）接速度
 |  |    |  |    |   |
 fX fY  rX rY   vX  vY
```

> 如果用 `tof_c3_supermini`（無速度），`[unpack i i i i]` 就夠了。
> 用 `tof_c3_supermini_vel` 時改成 `[unpack 0 0 0 0 0. 0.]` 或 `[unpack i i i i f f]`。

### 映射到 GL 座標

現有的 `tof_sensors.maxpat` 將 filtered 值映射為 -1.0 ~ 1.0：

```
filtered_x → [/ 360.] → [* 2.] → [- 1.] → x_gl (-1.0 ~ 1.0)
filtered_y → [/ 320.] → [* 2.] → [- 1.] → y_gl (-1.0 ~ 1.0)
```

### Max/MSP Patch 檔案

| Patch | 說明 |
|-------|------|
| `tof_sensors.maxpat` | Serial 接收 + 數值顯示 + GL 座標映射 + pictslider 視覺化 |
| `tof_line_draw.maxpat` | 接收 GL 座標，用 `jit.gl.mesh` 畫連續線條，有拖尾消失效果 |

---

## 參數調整

在 `.ino` 檔案頂部可調整以下參數：

### 感測器參數

| 參數 | 預設值 | 說明 |
|------|--------|------|
| `TIMING_BUDGET_US` | 33000 (33ms) | 感測器量測時間，越大越精確但越慢 |
| `OUTPUT_INTERVAL_MS` | 20 (50Hz) | 輸出間隔，不要低於 timing budget 的兩倍 |
| `WARMUP_MS` | 500 | 暖機時間 |
| `CALIB_MS` | 5000 | 校正收集時間 |
| `RANGE_MAX` | 2000 | 有效量測範圍上限 (mm) |

### 濾波參數（位置）

| 參數 | 預設值 | 說明 |
|------|--------|------|
| `MEDIAN_WINDOW` | 3 | Median 窗口，越大越抗突波但延遲越高 |
| `ALPHA_SLOW` | 0.12 | 靜止時 EMA 係數，越小越平滑 |
| `ALPHA_FAST` | 0.6 | 移動時 EMA 係數，越大越跟手 |
| `ADAPTIVE_THRESH` | 10.0 | 靜止/移動切換閾值 (mm) |
| `DEAD_BAND_MM` | 3 | Deadband 門檻，低於此變化量不更新 |

### 速度參數（`_vel` 版）

| 參數 | 預設值 | 說明 |
|------|--------|------|
| `VEL_SMOOTH` | 0.06 | 速度 EMA 平滑係數，越小 ramp 越緩（連續漸變），越大越即時 |

**VEL_SMOOTH 效果對照**（@ 50Hz）：

| VEL_SMOOTH | 63% 反應時間 | 適合場景 |
|------------|-------------|----------|
| `0.03` | ~0.67 秒 | 非常緩慢的漸變，適合環境音控制 |
| `0.06` | ~0.33 秒 | 預設值，平滑漸變 |
| `0.10` | ~0.20 秒 | 較快反應，適合節奏控制 |
| `0.20` | ~0.10 秒 | 即時反應，有少量平滑 |
| `0.35` | ~0.06 秒 | 幾乎即時，但可能有輕微跳動 |

> 反應時間公式：`-DT / ln(1 - VEL_SMOOTH)` 秒

### 調整建議

| 你覺得... | 調什麼 |
|-----------|--------|
| 靜止時還在抖 | `DEAD_BAND_MM` 加大到 4~5 |
| 手動了但反應太慢 | `ALPHA_FAST` 加大到 0.7~0.8 |
| 移動中數值不夠滑順 | `ALPHA_FAST` 降到 0.4~0.5 |
| 偶爾還有突波穿透 | `MEDIAN_WINDOW` 改成 5 |
| 靜止↔移動切換太敏感 | `ADAPTIVE_THRESH` 加大到 15~20 |
| 感測器讀值本身不穩 | `TIMING_BUDGET_US` 加大到 50000 |
| 速度變化太跳 | `VEL_SMOOTH` 降到 0.03 |
| 速度反應太慢 | `VEL_SMOOTH` 加大到 0.10~0.20 |
| 停下後速度沒歸零 | 檢查 `DEAD_BAND_MM`，要讓 fX/fY 真的鎖住才會觸發歸零分支 |

---

## 疑難排解

| 問題 | 可能原因 | 解法 |
|------|----------|------|
| Serial Monitor 無輸出 | ESP32-C3 未啟用 USB CDC | Tools → USB CDC On Boot → **Enabled**，重新燒錄 |
| `/error sensor1_init_failed` | 感測器接線鬆脫或 I2C 腳位錯誤 | 檢查 SDA/SCL/XSHUT 接線與供電 |
| 數值不動（一直是 0） | 校正時手把不在原點 | Serial 送 `c` 或按外接按鈕重新校正 |
| Max 收不到資料 | Serial port 被 Arduino Serial Monitor 佔用 | 關閉 Serial Monitor 再開 Max |
| Max 收到亂碼 | Baud rate 不對 | 確認 Max 的 serial object 設為 115200 |
| 編譯失敗 `{build.partitions}` | Board 沒選對 | 選 ESP32C3 Dev Module，設好 Partition Scheme |
