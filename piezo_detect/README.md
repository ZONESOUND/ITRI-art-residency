# Piezo Detect — 壓電敲擊與連續活動感測模組

ESP32-C3 SuperMini + 4 顆壓電片（Piezo），用於**同動車（Synchronous Movement Vehicle）的敲擊與刮／摸偵測**。

> 屬於「節奏繞纏」（Rhythmic Entanglements）專案的一部分。本模組設計為「一個感測介面、兩種互動形式」：使用者**敲打**壓電片時觸發離散音件（鼓擊、合成事件）；使用者**刮、摸、持續按壓**壓電片時，連續輸出活動量供 Max 端做音色變化、效果控制等連續映射。

---

## 韌體版本

### 目前使用版本

| 目錄 | 板子 | 通道 | 輸出格式 | 說明 |
|---|---|---|---|---|
| **[`piezo_4drum/`](piezo_4drum/)** | **ESP32-C3 SuperMini** | **4** | **`/piezo`（敲擊事件） + `/piezo/stream`（50 Hz 連續串流）** | **目前同動車使用的版本，含 WHO 識別協定** |

### 封存版本（`archive/`）

| 檔案／目錄 | 板子 | 通道 | 用途 |
|---|---|---|---|
| `archive/piezo_detect.ino` | ESP32 (any) | 1 | 早期單通道 8 kHz 原始波形串流，**用於機器學習特徵抽取**（FluCoMa、MuBu）。後來獨立成根目錄 [`piezo_detect_who/`](../piezo_detect_who/) 模組 |
| `archive/piezo_paul/` | — | — | Paul 提供的原始可動 code（`piezo_4drum` 的基礎） |
| `archive/led_test/` | — | — | LED 接線測試用 sketch |
| `archive/piezo_demo1.maxpat` | — | — | 早期版本 Max patch |

---

## Serial 輸出格式

Baud rate：**115200**

### 1. 敲擊事件（離散）

```
/piezo <channel> <velocity> <rawPeak>
```

| 欄位 | 範圍 | 說明 |
|---|---|---|
| `channel` | 1~4 | 哪個通道被敲 |
| `velocity` | 1~127 | 力度（從 peak ADC 值映射） |
| `rawPeak` | 0~4095 | 原始 ADC peak 值 |

觸發條件：連續 4 次超過門檻 + 距上次觸發超過 120 ms 冷卻。

### 2. 連續活動串流（每 20 ms 一次，50 Hz）

```
/piezo/stream <d1> <d2> <d3> <d4>
```

每個 `dN` = 該通道濾波後減去動態 baseline 的活動量（≥ 0）。靜止時接近 0、輕摸 30~200、重擊瞬間 2000+。

### 3. WHO 裝置識別協定

電腦端送 `WHO\n`，韌體回 `ID:piezo`。給 [`serial_auto_detect/`](../serial_auto_detect/) 自動配對 USB port 用。

完整訊息規格、可調參數、演算法細節：[`piezo_4drum/README.md`](piezo_4drum/README.md)

---

## Max Patches

| 檔案 | 用途 |
|---|---|
| `piezo_demo2.maxpat` | 最新的整合範例：`[route /piezo /piezo/stream]` 分流，敲擊觸發 Tiny Sound 合成、平均音量切換音色、瞬間變化觸發效果 |
| `archive/piezo_demo1.maxpat` | 早期版本，僅處理敲擊事件 |

---

## 設計理念：敲 vs 刮

過去版本只送敲擊事件，等於把壓電片當「打鼓鍵」用。但現場觀察使用者除了敲，還會用手指刮、摸、按壓——這些動作沒有明確的「擊發瞬間」，敲擊偵測會抓不到，但其實聲響上更豐富。

`piezo_4drum` 從第一版就同時提供兩種輸出：

- **敲（事件）**：Tiny Sound 合成、取樣播放等需要「明確觸發點」的音件
- **刮、摸（連續）**：filter cutoff、reverb send、音色切換等需要「連續變化」的控制

兩種訊息共用同一條 Serial 流，Max 端用 `[route /piezo /piezo/stream]` 分流，下游處理鏈各自獨立。

---

## 相關文件

- 主 repo：[`../README.md`](../README.md)
- 詳細 4drum 韌體文件：[`piezo_4drum/README.md`](piezo_4drum/README.md)
- 自動 Port 辨識工具：[`../serial_auto_detect/README.md`](../serial_auto_detect/README.md)
- 單通道 8 kHz ML 串流版本：[`../piezo_detect_who/`](../piezo_detect_who/)
