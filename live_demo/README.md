# live_demo — Ableton Live Demo 專案

「同動車 Live Demo」的 Ableton Live 現場 demo 專案。與 `paired_motion/`（Max/MSP 演出主程式）是**兩套獨立的東西**，各自開、各自存。

## 檔案位置

```
live_demo/
└── Live_Demo_Project/
    ├── Live_Demo.als          ← 專案本尊，用 Ableton Live 開這個
    ├── Ableton Project Info/  ← Ableton 專案 metadata
    └── Backup/                ← Ableton 自動備份（已被 .gitignore 忽略，不進 repo）
```

## 怎麼開始工作

- **直接開 repo 裡的 `Live_Demo.als`**，不要在別的地方另存分身，否則會兩邊改、對不起來。
- Mac mini 桌面上有一個原生 Finder 捷徑 `Live_Demo.als`（左下角有箭頭圖示），雙擊即可用 Ableton 開啟本尊。
  - 這是 macOS 原生 alias，不是 Unix symlink——後者會每次跳「Verifying…」而且可能開不起來。
  - 換到別台電腦時，這個桌面捷徑不會跟著 git 走，需要各自在該電腦重建（見下）。

## Git / 版本備份

一般流程（在 repo 根目錄）：

```
git add -A
git commit -m "說明這次改了什麼"
git push
```

- **音檔走 Git LFS**：`.gitattributes` 已設定，`live_demo/` 底下的音檔（wav/aif/aiff/mp3/flac/m4a）會自動走 Git LFS，不會撐爆 git 歷史。未來在 Ableton 按 **Collect All and Save** 收進 `Samples/` 的音檔都會自動走 LFS。
- **`Backup/` 不進 repo**：Ableton 自動備份由 `.gitignore` 排除（git 本身就在做版本控制）。

## 換到其他電腦時（例如非 Mac mini）

1. `git clone` 本 repo。
2. **裝 Git LFS**（否則音檔只會拿到指標檔）：
   ```
   brew install git-lfs
   git lfs install
   git lfs pull        # 把音檔實體抓下來
   ```
3. 用 Ableton 開 `live_demo/Live_Demo_Project/Live_Demo.als`。
4. （選用）在該電腦桌面自建捷徑：Finder 裡對 `Live_Demo.als` 按右鍵 →「製作替身 / Make Alias」→ 拖到桌面。

## GitHub LFS 額度

免費 1GB 儲存 + 1GB/月流量，一般 demo 足夠；音檔大量成長時再評估付費或改策略。
