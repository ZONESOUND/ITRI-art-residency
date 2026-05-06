# Piezo 4-Drum

ESP32-C3 SuperMini 四通道壓電感測器，輸出**敲擊事件**與**連續活動串流**兩種訊息。

## 硬體接線

| 功能 | GPIO | 說明 |
|------|------|------|
| Piezo 1 | GPIO4 | 壓電感測器 + 1M ohm to GND |
| Piezo 2 | GPIO3 | 壓電感測器 + 1M ohm to GND |
| Piezo 3 | GPIO0 | 壓電感測器 + 1M ohm to GND |
| Piezo 4 | GPIO1 | 壓電感測器 + 1M ohm to GND |
| LED 1 | GPIO6 | LED + 220 ohm |
| LED 2 | GPIO5 | LED + 220 ohm |
| LED 3 | GPIO10 | LED + 220 ohm |
| LED 4 | GPIO7 | LED + 220 ohm |

## Serial 輸出格式

裝置同時輸出兩種訊息：**離散敲擊事件** 與 **連續活動串流**。

### 1. 敲擊事件（hit event）

```
/piezo <channel> <velocity> <rawPeak>
```

- `channel`: 1~4
- `velocity`: 1~127（從 peak 值映射）
- `rawPeak`: 原始 ADC 值 (0~4095)
- 觸發條件：連續 `HITS_REQUIRED` 次超過 `THRESHOLD_DELTA`，且距上次觸發超過 `COOLDOWN_MS`

範例：
```
/piezo 1 88 3084
/piezo 3 112 3560
```

### 2. 連續活動串流（continuous stream）

```
/piezo/stream <d1> <d2> <d3> <d4>
```

- 每 20ms 一行（50Hz），不需觸發
- 每個 `dN` = 該通道 IIR 濾波值減去動態 baseline，clamp 到 ≥0
- 範圍參考：靜止 ~0、輕摸/刮 30–200、重擊瞬間 2000+、持續按壓數百到上千

範例：
```
/piezo/stream 0 0 0 0
/piezo/stream 12 0 187 5
/piezo/stream 0 2456 0 8
```

### 兩者的設計分工（敲 vs 刮）

- `/piezo`（hit event）：用來觸發**離散音件**（鼓擊、Tiny Sound 合成、取樣播放）
- `/piezo/stream`（continuous）：用來做**連續控制**（filter cutoff、reverb send、音色切換、視覺輝光）

實作參考：`../piezo_demo2.maxpat`
- 用 `[route /piezo /piezo/stream]` 分流
- stream 的「平均音量」切換 Tiny Sound 音色
- stream 的「瞬間音量變化」觸發合成事件
- 同一塊壓電片，敲出鼓打點、刮出連續音色變化

## 裝置識別（WHO Protocol）

電腦端發送 `WHO\n`，ESP32 回覆 `ID:piezo`。

用於 USB Hub 接多個 ESP32 時自動辨識 Serial Port 對應的裝置。

## 演算法特性

- **Dynamic baseline tracking** — 自動追蹤環境基線，適應震動變化
- **IIR filter** — 低通濾波降噪
- **Consecutive hit debounce** — 連續超過門檻才觸發，避免誤判
- **Non-blocking peak capture** — 15ms 內掃描峰值，不阻塞 loop
- **Non-blocking LED flash** — LED 閃爍不影響偵測
- **Serial buffer overflow protection** — TX buffer 快滿時跳過輸出，防止長時間運行後延遲

## 可調參數

| 參數 | 預設值 | 說明 |
|------|--------|------|
| `THRESHOLD_DELTA` | 250 | 超過 baseline 多少觸發（每通道獨立陣列） |
| `MAX_READING` | 3000 | velocity 映射的最大 ADC 值（每通道獨立陣列） |
| `SCAN_TIME_MS` | 15 | 峰值掃描時間 (ms) |
| `COOLDOWN_MS` | 120 | 同通道觸發冷卻 (ms) |
| `HITS_REQUIRED` | 4 | 連續幾次超門檻才觸發 |
| `BASELINE_ALPHA_SHIFT` | 6 | baseline 追蹤速度（位移運算，越大追得越慢） |
| `FILTER_SHIFT` | 2 | IIR 濾波強度（位移運算，越大越平滑） |
| `LED_MIN_MS` | 30 | LED 最短亮燈時間（輕觸） |
| `LED_MAX_MS` | 1000 | LED 最長亮燈時間（重擊） |
| `LED_ACTIVITY_THRESHOLD` | 85 | 活動量超過此值就點 LED。歷次調整：30 → 100（壓 EMI spike）→ 66 → 85（兼顧靈敏度跟穩定性）。**只影響 LED，不影響敲擊偵測** |
| `LED_HITS_REQUIRED` | 3 | 連續 N 幀過 threshold 才點 LED。單發 spike 永遠不會連續多幀，會被完全擋掉。從 2 提到 3 進一步抑制兩幀 spike |
| `STREAM_INTERVAL_MS` | 20 | 連續串流輸出間隔（50Hz） |
