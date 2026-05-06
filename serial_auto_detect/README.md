# Serial Auto-Detect

同動車三件感測器的 **Serial Port 自動辨識工具**。

讓 Max patch 不需要人為記住「哪個 `/dev/tty.usbmodem*` 是哪顆 ESP32」——透過 WHO 識別協定，由 [node.script] 自動掃描 + 配對 + 把正確 port 名餵給對應的 [serial] 物件。

---

## 為什麼需要這個

三顆 ESP32-C3 SuperMini（TOF / Pressure / Piezo）接到同一個 USB Hub 時，macOS 配發的 `/dev/tty.usbmodemXXXX` 名稱會：

- 跟著 ESP32 晶片的 USB serial number 走（不會因為換 USB 孔變動，但**換不同電腦會不同**）
- 三顆插入順序不同時，看不出哪顆是 TOF、哪顆是 Pressure
- 過去 patch 裡寫死 port 名 → 換場地 / 換筆電 / 換 hub 都要手動重新對應，演出時很危險

**靜默錯誤是最危險的**——port 對錯時，TOF 的資料會跑進 Pressure 的處理鏈，演出中很難察覺。

---

## 資料夾內容

| 檔案 | 用途 |
|---|---|
| `auto_detect.js` | 給 Max [node.script] 用的主邏輯，掃描 USB port 後對每顆 ESP32 做 WHO 識別 |
| `who_probe.js` | 命令列單 port 診斷工具（不需要 Max） |
| `auto_detect_test.maxpat` | Max 測試 patch（完整 wiring 範例） |
| `package.json` | npm dependencies |

---

## 核心原理

### WHO 識別協定

韌體端在 Serial 收到 `WHO\n` 時回應 `ID:tof` / `ID:pressure` / `ID:piezo`。三顆 ESP32 都實作了這個協定（自 2026-03-30 起），所以軟體端只要：

1. 對某 port 送 `WHO\n`
2. 讀回應內容
3. 用正規表達式 `/ID:(tof|pressure|piezo)\b/i` 比對
4. 確定該 port 對應哪顆裝置

### auto_detect.js 流程

```
1. SerialPort.list() 列舉所有 serial 裝置
   ↓
2. 過濾出 usbmodem / usbserial 開頭的（排除 BLTH / Bluetooth-Incoming-Port 等系統 port）
   ↓
3. 對每個 candidate port：
   a. 開啟 (baud=115200)
   b. 等 1200ms（讓 ESP32-C3 過完 USB CDC boot reset）
   c. 送 WHO\n
   d. 之後每 400ms 再送一次（避免 boot 時機 miss）
   e. 收到 ID:xxx 就停止 + 記錄
   f. 3 秒沒回應就放棄
   g. 關閉 port（讓 Max [serial] 等等可以接管）
   ↓
4. 透過 Max outlet 輸出結果：
   - tof <port_name>      （短名，已去掉 /dev/tty. 前綴）
   - pressure <port_name>
   - piezo <port_name>
   - missing <id>          某個 ID 沒掃到
   - done                  掃描結束
   - error <msg>           例外狀況
```

### Max patch 端接收

```
[node.script auto_detect.js @autostart 1]
            │ outlet
            ▼
[route tof pressure piezo missing done error]
   │      │       │       │      │     │
   ▼      ▼       ▼       ▼      ▼     ▼
 [port $1, open] x 3       (status / log 用)
   │      │       │
   ▼      ▼       ▼
[serial a 115200 8 1]
[serial b 115200 8 1]
[serial c 115200 8 1]
```

`port $1, open` message box 是 Max 巨集：`$1` 自動代換成 route 送來的 port 名，逗號讓它依序送兩個訊息（先 `port usbmodemXXXX` 再 `open`）。

---

## ⚠️ 注意事項

### 1. ESP32-C3 USB CDC boot reset

ESP32-C3 SuperMini 用 native USB CDC，**Mac 端開啟 port 瞬間 DTR 訊號會 trigger ESP32 reset**。從 reset 到 Serial 真正能收指令大約需要 1~1.5 秒。

`auto_detect.js` 預設 `BOOT_WAIT_MS = 1200`、`SCAN_TIMEOUT_MS = 3000`，並在 boot wait 後每 400ms 重送 WHO，所以即使第一發 miss 也會被後面的 retry 接到。

### 2. Node-for-Max 初始化延遲

`[node.script]` 啟動需要 ~1-2 秒（要先啟動 Node 程序、載入 npm 套件、執行 script 主體）。**這段期間送 `scan` 訊息會被回**：

```
node.script: Node script not ready can't handle message scan
```

對策：
- 用 `@autostart 1` 讓 script 載入完自己跑一次（這是預設）
- 等首次 scan 跑完才用 RESCAN 按鈕

### 3. Max [serial] 必須有 metro 驅動

`[serial]` 物件**不會自動 push buffer**——需要外部送 `bang` 它才會把累積的 byte 推出 outlet。標準做法：

```
[loadbang] → [1( → [metro 20] → [t b b b] → 三個 [serial]
```

20ms 間隔 = 50Hz polling，足以即時處理三顆裝置的 streaming 資料（TOF/Piezo 50Hz、Pressure 20Hz）。

### 4. Max [serial] 第一個 arg 是 port，不是 baud

寫成 `[serial 115200 8 1]`（沒字母）會被 Max 解讀為「port=115200」，超出 0–255 範圍報錯：

```
serial: port must be between 0 and 255
serial: specified port not available
```

**正確寫法是給 letter**：`[serial a 115200 8 1]`、`[serial b 115200 8 1]`、`[serial c 115200 8 1]`。letter `a/b/c` 只是 placeholder，後續用 `port usbmodemXXXX` 訊息會覆蓋掉。

### 5. Resource busy 問題

`[serial]` 在某些狀況會 auto-open 對應 letter 的 port（例如 patch 載入瞬間）。如果同時 node.script 在 scan，會搶 port 造成：

```
Error: Resource busy, cannot open /dev/tty.usbmodem1423XXX
```

對策：
- 重 scan 前用 `close` 訊息明確關閉三個 [serial]
- 在 patch 加一個 close button（[X]）給人手動觸發

### 6. 韌體必須有 WHO 支援

WHO 協定是 **2026-03-30** 才加進 `tof_c3_supermini_vel` 和 `pressure_2hands` 韌體的。如果 ESP32 燒的是更早版本（即使有 velocity 等其他新功能），會**沒有 WHO 處理 code**——auto_detect.js 收得到 streaming 但抓不到 ID。

`piezo_4drum` 從第一版（2026-03-30 12:51）就含 WHO，沒這個問題。

確認方式：用 Arduino IDE Serial Monitor，line ending 設 `Newline`，輸入 `WHO` 按 Enter。應該立刻看到 `ID:tof`（或對應 ID）。沒看到就是韌體舊，要重燒。

---

## 安裝

```bash
cd serial_auto_detect
nvm use 20      # 或 16+ 都可
npm install
```

需要 Node.js 16+（`serialport@^12` 的需求）。Max for Live 內建的 Node 版本通常已經夠新。

---

## CLI 診斷工具：`who_probe.js`

不開 Max、純命令列驗證單一 port 的工具。

### 列出可用 port

```bash
node who_probe.js
```

### 測試特定 port

```bash
node who_probe.js /dev/tty.usbmodem1423101
```

5 秒內會把所有收到的 raw bytes 帶 timestamp 印出來，t=1.5s 與 2.5s 各送一發 `WHO\n`。最後給診斷結論：

| 結果 | 意思 |
|---|---|
| `ID 偵測: ID:xxx ✓` | 韌體 OK，可以放心用 auto_detect |
| `沒看到 "ID:..." 字樣` | ESP32 在送資料但沒回 WHO → 韌體可能舊版沒 handler，需重燒 |
| `完全沒收到資料` | ESP32 沒在跑 → 線材/供電/baud rate/韌體掛了 |

⚠️ 跑 who_probe 之前必須**完全退出 Max（Cmd+Q）**，不然 port 被 [serial] 佔住會 "Resource busy"。

---

## 排查流程

遇到「auto-detect 失敗」或「資料沒進來」按這個順序排查：

```
1. 完全退出 Max（Cmd+Q）→ 釋放所有 port
   ↓
2. CLI 跑 who_probe.js 對每顆 ESP32 測一次
   ↓
3. 三種結果三種處理：
   a) ID:xxx ✓
      → 韌體 OK，問題在 Max 端
      → 檢查：metro 有沒有跑？[serial] letter 對嗎？close 釋放了嗎？
   b) Streaming 有但無 ID
      → 韌體舊版
      → 重燒最新版 .ino，再驗證
   c) 完全沒資料
      → 硬體問題
      → 檢查：USB 線、ESP32 LED 有沒有亮、Arduino IDE Serial Monitor 看得到嗎
```

---

## Port 對應表（user 的設置）

基於 USB serial number 衍生的末 4 碼，**只要不換掉 ESP32 晶片，這個對應永遠不變**：

| 末 4 碼 | 裝置 | 韌體 |
|---|---|---|
| `1423101` | Pressure | `pressure_2hands/pressure_2hands.ino` |
| `1423301` | TOF | `tof_distance_sensor/tof_c3_supermini_vel/tof_c3_supermini_vel.ino` |
| `1423401` | Piezo | `piezo_detect/piezo_4drum/piezo_4drum.ino` |

---

## 設計取捨

### 為什麼用 node.script 而不是 Max [v8] 或純 Max patch

- Max [v8] / [js] 沒有直接的 SerialPort 套件支援
- 純 Max [serial] 可以做但時序控制（open / close / 切 port）寫成 patch 很複雜
- node.script + `serialport` 套件可以直接呼叫 OS 的 serial port API，邏輯用 async / await 寫起來線性可讀

### 為什麼 baud 寫死 115200

三顆韌體現在都 115200。歷史上 piezo 有過 921600 raw stream 版本（給 ML 用），auto_detect.js 之前有 fallback 邏輯試 921600。後來 piezo_4drum 統一到 115200，fallback 拿掉了。如果未來加新裝置用不同 baud，可以在 `BAUD_RATES` 陣列加進去再 fallback。

### 為什麼掃描順序是 sequential 不是 parallel

每顆 ESP32 開 port 瞬間會被 DTR reset，要等 ~1.5 秒 boot。如果三顆同時開 port，三顆同時 reset，時序更難控制（誰先 boot 完誰先回 WHO，混在 buffer 裡難分流）。Sequential 雖然慢一點（3 秒 × 3 顆 ≈ 9 秒最壞情況），但每顆獨立、debug 訊息清楚、結果穩定。

---

## 相關文件

- 主 repo README：[`../README.md`](../README.md)
- WHO Protocol 韌體實作：見各裝置 .ino 檔內 `handleSerialCommand()` 函式
- ESP32 port 對應記憶卡：（user 個人 Obsidian / Claude memory）
