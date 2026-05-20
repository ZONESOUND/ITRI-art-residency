# ToF Trajectory Visualization (paired_motion build)

VL53L0X 雙 ToF 感測器的即時軌跡視覺化工具。
支援 **軌跡拖尾 (Trail)** 和 **熱力圖 (Heatmap)** 兩種模式，並自動鏡像顯示（左右手對稱）。

> 本資料夾是 `tof_distance_sensor/visualization/` 在 paired_motion 內的 fork：server.js 改成額外廣播 vXn/vYn（normalized 速度，-1~1），跟韌體 `tof_c3_supermini_vel_norm` 一致。

---

## 架構

```
ESP32-C3 (TOF) ──serial──► sub_auto_detect ──[route /tof]──► [s tof]
                              (paired_motion 既有)              │
                                                                 ▼
                                                            [r tof]
                                                                 │
                                                       [prepend /tof]   ← 把 route 剝掉的前綴補回去
                                                                 │
                                                  [node.script server.js]
                                                                 │  SSE (Server-Sent Events)
                                                                 ▼
                                                       瀏覽器 index.html (Canvas)
```

- **server.js**：Node for Max 腳本，接收 Max 訊息後透過 SSE 推送到瀏覽器
- **index.html**：單檔前端，Canvas 全螢幕即時繪製
- **零外部依賴**：不需要 `npm install`，SSE 不需要 WebSocket library

---

## Max 接法

已經做好兩個現成的 patch，挑一個用：

### A. `patchers/main_viz.maxpat`（推薦：完整演出版 + 視覺化）

`main.maxpat` 的副本，右半邊多了視覺化區塊（`[r tof]` + `[node.script]` + start/stop/restart + `print viz`）。
**原本的 `main.maxpat` 完全不動**——想跑視覺化就開 `main_viz.maxpat`，不想跑就開 `main.maxpat`。

### B. `patchers/sub_visualization.maxpat`（模組化：跟原 main.maxpat 並用）

獨立的小 patch，內容跟 A 的視覺化區塊一樣。可以：
- 直接 File → Open 當第二個視窗開
- 在你自己的 patch 裡放 `[bpatcher sub_visualization.maxpat]`

只要 `sub_auto_detect` 在跑（不管在哪個 patch 內），全域 `[s tof]` 就會把資料送到 sub_visualization 的 `[r tof]`。

### server.js 怎麼吃這些訊號

`server.js` 同時註冊了 `'/tof'` 和 `'list'` 兩個 handler，所以下面這幾種接法都 work：

| 接法 | 走哪個 handler | 範例位置 |
|---|---|---|
| `[r tof] → [node.script ...]` | `'list'`（裸 list） | main_viz / sub_visualization 用這個 |
| `[fromsymbol] → [node.script ...]` | `'/tof'` | route 之前；`tof_visual.maxpat` 用這個 |
| `[r tof] → [prepend /tof] → [node.script ...]` | `'/tof'` | 等效於上方 ① |

---

## 啟動 node.script

跟 `code/auto_detect.js` 一樣，**沒有 `@autostart`**（避免 Max clone 階段 crash）。
patch 載入後按一次 `script start` 即可；改完 server.js 要重新載入按 `script restart`。

---

## 使用方式

1. Max 開 `paired_motion.maxproj` → `main_viz.maxpat`（或 `main.maxpat` + 另外開 `sub_visualization.maxpat`）
2. 等 sub_auto_detect 掃描完三顆 ESP32（console 印 `tof: usbmodem...`）
3. 按 `script start`，console 應印 `[HTTP] http://localhost:8080`
4. 瀏覽器開 **http://localhost:8080**
5. 開始移動感測器

> 想先單獨測 viz 不接整個 paired_motion？打開 `tof_visual.maxpat`（同資料夾的 standalone 測試 patch）。

---

## 鍵盤快捷鍵

| 按鍵 | 功能 |
|------|------|
| `1`  | 切換到 Trail（軌跡拖尾）模式 |
| `2`  | 切換到 Heatmap（熱力圖）模式 |
| `C`  | 清除所有軌跡 / 熱力資料 |
| `F`  | 切換全螢幕 |

---

## 可調參數一覽

所有參數都在 `index.html` 的 `<script>` 區塊頂部，搜尋變數名即可找到。

### 感測器範圍

| 參數 | 目前值 | 說明 |
|------|--------|------|
| `RANGE_X` | `320` | X 軸最大位移（mm）。Arduino 校正後輸出的 fX 最大值 |
| `RANGE_Y` | `220` | Y 軸最大位移（mm）。Arduino 校正後輸出的 fY 最大值 |
| `PAD` | `0.05` | 邊緣留白比例（0~0.5）。0.05 = 上下左右各留 5% 空白 |

> **座標方向**：
> - fX = 0 → 螢幕右邊緣（靠近 X 感測器），fX = RANGE_X → 中線
> - fY = 0 → 螢幕底部（靠近 Y 感測器），fY = RANGE_Y → 頂部
> - 左半邊為右半邊的鏡像

### 軌跡模式 (Trail)

| 參數 | 目前值 | 說明 |
|------|--------|------|
| `TRAIL_MAX` | `300` | 軌跡保留的最大點數。越大尾巴越長，記憶體用量也越高 |
| fade alpha | `0.08` | 每幀覆蓋的半透明黑色透明度（在 `drawTrail()` 裡）。越大淡出越快 |
| `VEL_MAX` | `500` | 速度→顏色/粗細映射的最大速度值（mm/s）。超過此值一律紅色最粗 |

**速度視覺效果**（使用 ESP32 的 vX/vY，EMA 平滑）：
- **顏色**：慢速 = 藍色 (hue 200)，快速 = 紅色 (hue 0)
- **線條粗細**：靜止 1px → 最快 5px（乘以 age 淡入）
- **光暈大小**：靜止 6px → 最快 20px

### 熱力圖模式 (Heatmap)

| 參數 | 目前值 | 說明 | 調整建議 |
|------|--------|------|----------|
| `GRID` | `80` | 熱力圖解析度（80×80 格）。越大越精細，但 CPU 負擔越重 | 40~128 |
| `HEAT_DECAY` | `0.998` | 每幀衰減係數。越接近 1 熱力淡出越慢 | 0.990（快淡出）~ 0.9995（幾乎不淡） |
| `HEAT_ADD` | `0.15` | 每筆資料的熱力加權。越大，快速移動時軌跡也能看到 | 0.05（淡）~ 0.3（濃） |
| `HEAT_RADIUS` | `3` | 高斯擴散半徑（格數）。越大軌跡越粗 | 1（細線）~ 5（粗擴散） |

**速度加權**（使用 ESP32 vX/vY）：
- 快速移動時，熱力累加量提升至 3 倍，擴散半徑從 3 增加到 5 格
- 靜止時維持基本值（1x 熱力，3 格擴散）

**熱力圖顏色漸層**：黑 → 藍 → 青 → 綠 → 黃 → 紅

**HEAT_DECAY 效果說明**：

| HEAT_DECAY | 半衰期 (幀數) | 60fps 時約等於 |
|------------|--------------|----------------|
| `0.990`    | ~69 幀       | ~1.2 秒         |
| `0.995`    | ~138 幀      | ~2.3 秒         |
| `0.998`    | ~346 幀      | ~5.8 秒         |
| `0.999`    | ~693 幀      | ~11.5 秒        |
| `0.9995`   | ~1386 幀     | ~23 秒          |

> 半衰期公式：`ln(0.5) / ln(HEAT_DECAY)`

### SSE / 網路

| 參數 | 目前值 | 位置 | 說明 |
|------|--------|------|------|
| `HTTP_PORT` | `8080` | server.js | HTTP + SSE 的 port。如有衝突可改其他 port |

---

## 檔案結構

```
visualization/
├── server.js       ← Node for Max 中繼（Max → SSE → 瀏覽器）
├── index.html      ← 前端視覺化（單檔，含 CSS + JS）
├── package.json    ← 專案描述（不需要 npm install）
└── README.md       ← 本文件
```

---

## 資料格式

### Max → server.js

```
/tof fX fY rX rY                    ← tof_c3_supermini（4 atoms）
/tof fX fY rX rY vX vY              ← tof_c3_supermini_vel（6 atoms）
/tof fX fY rX rY vX vY vXn vYn      ← tof_c3_supermini_vel_norm（8 atoms，paired_motion 用這版）
```

- `fX`, `fY`：濾波後位移（int, mm, ≥0）
- `rX`, `rY`：校正後原始值（int, mm, ≥0）
- `vX`, `vY`：速度（float, mm/s, 帶正負）
- `vXn`, `vYn`：normalized 速度（float, -1.0 ~ +1.0；韌體已 deadband + clip）
- 頻率：約 50Hz（Arduino 端 20ms 間隔）
- server.js 自動相容三種格式，缺的欄位以 0 填補

### server.js → 瀏覽器 (SSE)

```json
{"type":"tof","fX":123,"fY":45,"rX":456,"rY":789,"vX":12.3,"vY":-5.1,"vXn":0.025,"vYn":-0.01}
```

目前 index.html 使用 `fX` / `fY`，並以 `vX` / `vY` 推導顏色與光暈。`vXn` / `vYn` 已透過 SSE 推送，前端如果想完全用 normalize 後的乾淨速度（靜止時 exact 0），可直接取用。

---

## 常見調整情境

### 想要軌跡更長 / 更短
→ 調整 `TRAIL_MAX`（目前 300）

### 熱力圖淡出太快 / 太慢
→ 調整 `HEAT_DECAY`（目前 0.998，約 5.8 秒半衰期）

### 快速移動時熱力圖看不太到
→ 調大 `HEAT_ADD`（目前 0.15）或 `HEAT_RADIUS`（目前 3）

### 感測器實際範圍改變了
→ 調整 `RANGE_X` / `RANGE_Y` 為新的最大位移 mm 值

### 畫面太擠 / 邊緣被裁掉
→ 調整 `PAD`（目前 0.05 = 5% 留白）
