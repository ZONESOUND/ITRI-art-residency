# sound_tools：離線聲音工具（soundtools）

《節奏繞纏》2026 年 8 到 10 月間為小星星與注音素材寫的離線處理與分析程式，整理成一個可跨專案呼叫的 Python 套件加指令列，另附同一套 varispeed 演算法的網頁版與 `gen~` 版。

| 子命令 | 做什麼 | 來源 |
|---|---|---|
| `drift` | 一段 loop 做多聲部 varispeed 漂移：OU random walk、耦合（各聲部拉向平均）、指定秒數回歸原速、在下一個樂句邊界硬對齊。可各聲部另存單軌 | `錄音/效果測試_20260902/scripts/render_effects.py`（2026-09-02） |
| `tape` | 磁帶鏈：wow flutter、飽和、磁頭高頻衰減，可加 tape echo 與殘響 | `錄音/Dicy2_memory/render_breath_tape.py`（2026-09-07） |
| `stretch` | paulstretch 極慢拉伸，可加低通 | `錄音/背景pad_20260908/scripts/render_backing_pads.py`（2026-09-08） |
| `phrases` | 旋律型態找樂句邊界（pyin 音高追蹤），可直接切檔 | 效果測試期間的即時分析程式，首次整理成檔 |
| `syllables` | 語音音節：停頓段、每段能量峰數、可選 allosaurus 音素辨識；給預期數量會標出不合的段 | 同上（2026-09-03 注音分段校正） |
| `stems` | DAW 匯出的 stems 以數位零切 region，正規化交叉相關回對原始素材，偵測多段拼接 | `錄音/20260906_小星星二版分軌/scripts/analyze_stems.py`（2026-09-06） |

`tape_drift/`：`tape_drift.html` 單檔網頁（拖音檔即播、三個預設、輸出 WAV，雙擊用瀏覽器開即可）；`tape_drift_gen.txt` 是同一演算法的 `gen.codebox~` 版，接法見同夾說明（2026-09-03）。

原專案裡的編排腳本（拼貼 A/B/C、compose、背景 pad 的 render 本體、小孩聲音擷取）是本案專屬，留在 iCloud 專案夾，不收進來。

## 安裝與執行

```bash
cd sound_tools
uv sync                     # 建 .venv，鎖在 uv.lock
uv run soundtools --help
uv run soundtools drift loop.wav --dur 100 --voices 5 --coupling 0.5 --sync 58 --stems
uv run soundtools tape voice.wav --echo 0.33 --reverb 2
uv run soundtools phrases song.wav --cut
uv run soundtools syllables reading.wav --expected 4,4,3,3
```

要在任何資料夾直接叫 `soundtools`：`uv tool install --editable ./sound_tools`。音素辨識另裝：`uv sync --extra phones`（會拉 torch）。

當函式庫用：

```python
from soundtools import io, varispeed, tape, collage, analysis
x, sr = io.load("loop.wav", mono=True)
r = varispeed.drift_ensemble(x, sr, dur=100, voices=5, coupling=0.5, t_sync=58)
io.write("mix.wav", varispeed.pan_mix(r["voices"], [-0.8, -0.4, 0, 0.4, 0.8], sr), sr, peak_db=-1)
```

## 驗證（2026-10-10）

- `phrases` 對 `中藥行小星星.wav`：句首 0.52、19.85、28.74、96.57 秒，與 2026-09-02 人工核對的邊界（0.52、19.90、28.79）相符。
- `drift` 三聲部、22 秒回歸：硬對齊前聲部時間差 −3.2 毫秒，對齊後 0.0 毫秒（由讀取位置直接計算）。
- `stems` 自測：從一段錄音切兩段放進靜音 stem，回對位置誤差小於 0.05 秒，ncc 1.00。
- `tape`、`stretch` 輸出無不連續樣本。

## 已知限制

- 全部離線處理，不是即時效果器；即時版只有 `tape_drift_gen.txt`（單聲部）。
- `syllables` 不做強制對齊：峰數與預期不合時要人工決定多出來的是哪一個（2026-09-03 的教訓：強制對齊會把重念與失誤靜靜吸收進去）。
- `phrases` 的型態要照素材寫；預設是小星星的兩種句頭。
- 方法說明與踩過的坑：Obsidian `Tools/MIR 音訊分析方法.md`。
