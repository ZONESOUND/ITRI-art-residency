# tape_drift_gen — 轉速不穩的錄音機 說明

> 《節奏繞纏》結尾用：走音的《小星星》慢慢變準，或走音版與準確版交織。
> 對應 Python 原型（`drift.py`）與網頁版 `tape_drift.html`，三者演算法相同、同一個種子出同一條曲線。
> 定位：**播檔用的變速效果**（讀取速度隨時間漂移，音高與速度一起動，像老卡帶），不是 insert 效果器。

---

## 這是什麼

把音檔放進 `buffer~`，用一個隨時間慢慢變化的速率去讀它。速率由三個慢速來源疊加決定：兩個正弦（預設 27 秒與 9 秒一圈）加一個內插雜訊。速率累積成讀取位置，位置用 `peek` 取相鄰兩個取樣、自己做線性內插讀出來。

可選的兩個變化：

- **收斂**：`converge` 秒內把漂移深度滑到 0，就是「從走音到準」。
- **原音層**：同時播一軌不漂移的版本，跟漂移層疊在一起，就是「交織」。

跑在 `gen.codebox~`（純 Max，低延遲，不依賴外部 server）。

---

## 在 Max / M4L 裡怎麼接

1. 開一個 **`gen.codebox~`**，把 `tape_drift_gen.txt` 整段貼進去，編譯（Cmd+Enter）。
2. 放一個 **`[buffer~ tapedrift]`**，把音檔載進去。載檔三選一：
   - `[replace]` 訊息接進 `buffer~` 會跳檔案選擇視窗；
   - M4L 用 `[live.drop]` → `[prepend replace]` → `buffer~`，可以直接把音檔拖進 device；
   - 或 `[replace /absolute/path/file.wav(` 寫死路徑。
3. 接線（**所有控制都進 gen.codebox~ 那唯一的左 inlet**）：

```
[live.dial 0–300]      → [prepend depth]     ─┐
[live.dial 0.005–0.5]  → [prepend rateSlow]  ─┤
[live.dial 0.01–3]     → [prepend rateFast]  ─┤
[live.dial 0–1]        → [prepend random]    ─┤
[live.dial -200–200]   → [prepend center]    ─┤
[live.dial 0–300]      → [prepend converge]  ─┤→ gen.codebox~ ─┬ out1 → [live.gain~] → [plugout~ 1]
[live.dial 0–1]        → [prepend dry]       ─┤                 ├ out2 → [live.gain~] → [plugout~ 2]
[live.dial 0–2]        → [prepend gain]      ─┤                 ├ out3 → [snapshot~ 50] → [live.numbox]（目前偏移，cent）
[live.toggle]          → [prepend loop]      ─┤                 └ out4 → [edge~] → 播完 bang
[live.toggle]          → [prepend play]      ─┤
[live.numbox 整數]     → [prepend seed]      ─┘
```

4. **播放**：`play` 由 0 變 1 會從頭開始（狀態全部歸零，同一個種子每次都一樣）；設 0 停。要重新觸發收斂就把 `play` 關掉再打開。
5. M4L 的 `live.dial` 都可以在 Live 裡自動化。`converge` 這個參數本身不需要自動化，它是「播放開始後幾秒內收斂完」，設好一個數字再按 `play` 就會走。

> **不是 M4L、只在 Max 裡試**：`plugout~` 換成 `ezdac~`，`live.dial` 換成 `flonum` 直接手打即可。

---

## 參數列表

| 參數 | 範圍 | 預設 | 意思 |
|---|---|---|---|
| `depth` | 0–300 | 45 | cent，漂移峰值 |
| `rateSlow` | 0.005–0.5 | 0.037 | Hz，慢速正弦（27 秒一圈） |
| `rateFast` | 0.01–3 | 0.11 | Hz，快速正弦（9 秒一圈） |
| `random` | 0–1 | 0.35 | 雜訊佔比，避免聽出規律 |
| `center` | -200–200 | 0 | cent，固定偏移；交織版設 -35 |
| `converge` | 0–300 | 0 | 秒，>0 時深度在這段時間內滑到 0；0 = 不收斂 |
| `dry` | 0–1 | 0 | 原音層音量；交織版設 1 |
| `gain` | 0–2 | 1 | 輸出音量；兩層疊加時降到 0.55 左右免得爆 |
| `loop` | 0/1 | 1 | 循環 |
| `play` | 0/1 | 0 | 0→1 從頭播；0 停 |
| `seed` | 整數 | 7 | 亂數種子，換一個就換一條漂移曲線 |

三個預設（跟網頁版一樣）：

- **漂移**：depth 45、random 0.35，其餘預設。
- **交織**：depth 0、center -35、dry 1、gain 0.55。原音跟降 35 cent 的同一段一起響，會有拍頻。
- **收斂**：depth 60、random 0.4、converge 60。播放後 60 秒走到準。

---

## 出口

| 出口 | 內容 |
|---|---|
| out1 / out2 | 左 / 右聲道。單聲道音檔兩邊一樣。 |
| out3 | 目前偏移（cent），signal。接 `snapshot~` 看數字，或接投影控制當「離準多遠」的驅動訊號。 |
| out4 | 播完（`loop` 為 0 時，最後一個取樣瞬間為 1）。接 `edge~` 取 bang。 |

---

## 跟網頁版的對應

| 網頁版（JS） | codebox（GenExpr） |
|---|---|
| `this.pos += rate` | `pos = pos + rate` |
| `Math.imul(rng, 1664525) + 1013904223 >>> 0` | `wrap(rng * 1664525. + 1013904223., 0., 4294967296.)` |
| 線性內插 `b[i0]*(1-frac)+b[i1]*frac` | `peek(buf, i0, ch)*(1-frac) + peek(buf, i1, ch)*frac`，同一條式子 |
| `Math.exp(cents * 0.000577623)` | `exp(cents * 0.000577623)` |
| `core.play()` | `play` 由 0 變 1 |

兩邊的亂數是同一個 LCG、同一個種子，所以網頁輸出的 WAV 跟 Max 裡即時播的曲線一致（前提是取樣率相同）。

---

## 可能要動的地方

- `peek` 的第三個參數是聲道索引（從 0 起算），第二個參數是**取樣索引**（不是 0–1 相位）。索引超出範圍時 `peek` 回傳 0。
- 想寫短一點可以改用 `sample`，它吃 0–1 相位並內建線性內插，四行 peek 可縮成：
  `outL = sample(buf, pos / len, 0);` `outR = sample(buf, pos / len, rch);`
  兩者聽起來一樣。這裡用 `peek` 是為了跟網頁版逐取樣完全一致，且不依賴相位正規化的細節。
- 音檔取樣率跟 Live 的取樣率不同時，`buffer~` 不會自動重取樣，播放會整體偏快或偏慢。先把音檔轉成跟 session 一樣的取樣率再載。
- 要接握力做「兩人的手越合、漂移越小」：把 `sub_pressure` 的雙手差值 `[abs]` → `[scale 0. 1. 0. 80.]` → `[prepend depth]`。這部分目前不需要，先留著。
