# Breath Sensor — ESP32-C3 SuperMini

單路吹氣/吸氣感測系統，將呼吸強度映射為霧化器 PWM 輸出，並以 TOF 距離控制 LED 亮度。

## 硬體

| 模組 | 腳位 | 說明 |
|------|------|------|
| HX710B SCK | GPIO 3 | 壓力感測器時鐘 |
| HX710B DOUT | GPIO 4 | 壓力感測器資料 |
| VL53L0X SDA | GPIO 5 | TOF I2C |
| VL53L0X SCL | GPIO 6 | TOF I2C |
| VL53L0X XSHUT | GPIO 10 | 可選，控制開關 |
| MOS PWM | GPIO 7 | 霧化器 MOSFET 控制 |
| NeoPixel DIN | GPIO 2 | 12 顆 LED Ring |
| 校正按鈕 | GPIO 9 | INPUT_PULLUP，按下接 GND |

供電：HX710B / VL53L0X 用 3.3V，NeoPixel 建議 5V，MOS 模組依規格外接。

## 演算法

### 呼吸偵測（HX710B）

1. **Baseline 校準**：開機讀 40 次取平均，按校正按鈕可重新校準（5 秒）
2. **Deadzone**：`|raw - baseline| <= 30000` 輸出 0，過濾靜止雜訊
3. **自適應映射**：動態追蹤 maxBlow / minInhale，吹氣映射 +1~+10，吸氣映射 -1~-10

### 霧化器 PWM

- PWM 頻率：20kHz（超出人耳範圍，避免噪音）
- PWM 解析度：10-bit（0~1023）
- 靜止時維持 2% baseline duty，保持霧化片低功率振動

**Duty 映射（兩段線性）：**

| out 值 | duty |
|--------|------|
| 0（靜止）| 2% |
| 0 < \|out\| < 1 | 3% |
| 1 ~ 8 | 3% → 50%（線性）|
| 8 ~ 10 | 50% → 100%（線性）|

### LED 控制（NeoPixel 12 顆）

兩層疊加：底色 + 旋轉白點。

**底色層（TOF 色溫漸變）：**
- 近（0mm）→ 暖琥珀橘 `(255, 120, 0)`
- 中（100mm）→ 紫 `(150, 0, 200)`
- 遠（200mm）→ 冷藍 `(0, 50, 255)`
- TOF 無效/超範圍 → 冷藍
- 亮度：近=亮（200），遠=暗（30）
- Exponential smoothing（係數 0.15），色溫和亮度都平滑過渡

**旋轉白點層（呼吸驅動）：**
- 吹氣：白點順時針旋轉
- 吸氣：白點逆時針旋轉
- 靜止（|out| < 0.3）：白點消失，只剩底色
- **指數速度曲線**：`speed ∝ out² / 10`，小力慢轉、大力爆轉（保留方向正負號）
- **動態拖尾長度**：吹越大力拖尾越長，2 顆 → 最多 8 顆
- 拖尾衰減曲線：`{1.0, 0.8, 0.6, 0.4, 0.25, 0.15, 0.08, 0.03}`
- 白色疊加在底色上（加法混色，clamp 255）

### 校正按鈕

GPIO 9，INPUT_PULLUP。按下時 LED 全白，重新校準 baseline（5 秒），校準完恢復。

## Serial 輸出

115200 baud，每 50ms 一筆（20Hz）：

```
/breath {raw} {out} {dutyPercent} {dutyRaw} {tofValue}
```

| 欄位 | 說明 | 範圍 |
|------|------|------|
| raw | HX710B 原始值 | 24-bit，0 = 讀取失敗 |
| out | 呼吸映射值 | -10.0 ~ +10.0 |
| dutyPercent | PWM 百分比 | 0.0 ~ 100.0 |
| dutyRaw | PWM 原始值 | 0 ~ 1023 |
| tofValue | TOF 距離 | mm，0 = 無效 |

Setup 階段輸出 debug 訊息：

```
[setup] start
[setup] I2C init...
[setup] TOF init...
[setup] TOF ready: 1
[setup] calibrating HX710B...
[setup] baseline: 8371234
[setup] done
```

## 可調參數

| 參數 | 預設值 | 說明 |
|------|--------|------|
| `DEADZONE_RAW` | 30000 | 靜止過濾範圍 |
| `DUTY_BASELINE` | 2.0% | 靜止時的最低 duty |
| `DUTY_MIN_POS` | 3.0% | 偵測到氣流時的最低 duty |
| `OUT_FULL_SCALE` | 10.0 | out 最大值對應 100% duty |
| `SMOOTH_FACTOR` | 0.15 | LED 色溫/亮度平滑係數（越小越滑順）|
| `DOT_SPEED` | 1.0 | 白點旋轉速度倍率（實際速度 = `sign(out) * out² / 10 * DOT_SPEED`）|
| `MAX_TAIL` | 8 | 最大拖尾長度（實際長度依氣流強度動態調整，最少 2 顆）|
| `LOOP_INTERVAL_MS` | 50 | 主迴圈間隔（ms）|

## 相依套件

- Adafruit_VL53L0X
- Adafruit_NeoPixel
- ESP32 Arduino Core 3.x
