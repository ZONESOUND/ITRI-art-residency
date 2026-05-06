# Paired Motion

工研院藝術進駐「**節奏繞纏**」（Rhythmic Entanglements）專案的演出主 patch。

整合三組感測器（Pressure / TOF / Piezo）成一個雙手互動樂器（同動車），以 Max/MSP 即時聲音合成。本資料夾是**演出版本**——zip 起來給合作者就能完整跑、跨電腦移植不需重新設定。

---

## 資料夾結構

```
paired_motion/
├── paired_motion.maxproj            ← Max Project 檔（Max 開這個進去）
├── main.maxpat                       ← 演出主 patch
├── README.md                         ← 你正在看
│
├── code/                             ← Node.js 自動化（auto-detect）
│   ├── bootstrap.js                  ← 進入點：自動裝依賴 + 載 auto_detect
│   ├── auto_detect.js                ← USB port 自動掃描 + WHO 識別
│   ├── who_probe.js                  ← 命令列診斷工具
│   ├── package.json
│   └── node_modules/                 ← 第一次執行後自動產生
│
├── abstractions/                     ← 各感測器處理邏輯
│   ├── sub_auto_detect.maxpat        ← auto-detect 封裝
│   ├── sub_tof.maxpat                ← TOF 訊號處理 + 聲響
│   ├── sub_pressure.maxpat           ← Pressure 訊號處理 + 聲響
│   └── sub_piezo.maxpat              ← Piezo 敲擊 + 連續活動 → 聲響
│
├── media/                            ← 取樣、loops、實地錄音
│
└── presets/                          ← 演出參數 snapshot
    └── 20yymmdd_場地名.maxsnap
```

---

## 第一次使用

1. **接好硬體**：三顆 ESP32（Pressure / TOF / Piezo）插到 USB Hub
2. **Max 開啟** `paired_motion.maxproj`
3. **打開 main.maxpat**
4. **等 bootstrap 跑完**：第一次需要 30~60 秒裝 npm 依賴，console 會印進度
5. **看 BOOTSTRAP 視窗**：應該看到「依賴已就緒」→「載入 auto_detect.js...」→「掃描結果」三組 ID 都被找到
6. 開始演出

之後每次開只要 1~2 秒（bootstrap 偵測到依賴已存在會直接跳過 npm install）。

---

## 跟其他資料夾的關係

| 資料夾 | 角色 |
|---|---|
| `paired_motion/`（本資料夾） | **演出版本** —— 凍結在已知可用狀態，給合作者用 |
| [`../serial_auto_detect/`](../serial_auto_detect/) | **實驗室** —— 開發 / debug auto-detect 機制 |
| [`../pressure_sensor/`](../pressure_sensor/) | Pressure ESP32 韌體 |
| [`../tof_distance_sensor/`](../tof_distance_sensor/) | TOF ESP32 韌體 |
| [`../piezo_detect/`](../piezo_detect/) | Piezo ESP32 韌體 |

`code/auto_detect.js` 是從 `serial_auto_detect/` 複製過來的**凍結副本**——`serial_auto_detect/` 之後的更動不會自動同步進來，避免實驗中的改動污染演出版本。需要更新時：

```bash
cp ../serial_auto_detect/auto_detect.js code/auto_detect.js
git commit -m "sync(paired_motion): pull latest auto_detect.js"
```

---

## 給合作者的快速啟動

如果你拿到的是 zip / 從 git clone 下來的乾淨副本：

1. 確認 Mac 上裝了 Node.js 16+（[下載](https://nodejs.org/)）
2. Max/MSP 9 開啟 `paired_motion.maxproj`
3. 雙擊 `main.maxpat`
4. 接 ESP32（不接也能開 patch，只是 auto_detect 會回報三顆都 missing）
5. 第一次開等依賴安裝（看 Max console）

不需要開 Terminal、不需要手動 `npm install`。

---

## ESP32 Port 對應

每顆 ESP32 的 USB port 名（短名）由 USB 序號決定，**不會因為換 USB 孔變動**：

| 末 4 碼 | 裝置 |
|---|---|
| `1423101` | Pressure |
| `1423301` | TOF |
| `1423401` | Piezo |

所有 ESP32 韌體都實作 WHO 識別協定——auto_detect.js 對每顆送 `WHO\n`，根據回應的 `ID:tof` / `ID:pressure` / `ID:piezo` 配對 port 名給 Max 的 `[serial]` 物件。

詳見 [`../serial_auto_detect/README.md`](../serial_auto_detect/README.md)。

---

## 還原 / 版本控制

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

---

## 待完成（Phase 2 之後）

- [ ] `abstractions/sub_auto_detect.maxpat` — 把 auto-detect 邏輯封裝成 abstraction
- [ ] `abstractions/sub_tof.maxpat` — TOF 處理 + 聲響映射
- [ ] `abstractions/sub_pressure.maxpat` — Pressure 處理 + 聲響映射
- [ ] `abstractions/sub_piezo.maxpat` — Piezo 處理 + 聲響映射
- [ ] `main.maxpat` 內 bpatcher 連接 + 混音 + dac~
- [ ] 取樣素材整理進 `media/`
- [ ] `presets/default.maxsnap` 預設參數
