# Harness 拆解簡報 — 工作存檔

給下一台電腦繼續用的存檔，內含成品、產生腳本、原始 Claude Code session。

## 內容

- `Harness 心智圖＋課程.html` — 目前的簡報成品（自包含，可直接雙擊在瀏覽器打開，click-to-advance）。
- `build/` — 產生這份簡報的 Python 腳本：
  - `diagram_lib.py` — 共用 SVG 圖表建構器（`Diagram` class）。
  - `build_slides2.py` — 所有投影片內容、圖表定義、`CLUSTERS`/`SLIDES` 資料，並在結尾驗證所有 `links` 目標與箭頭 marker 是否都合法。輸出 `/tmp/slides.json`。
  - `build_final.py` — 讀 `/tmp/slides.json`，產生完整 HTML，寫到 `~/Desktop/Harness 心智圖＋課程.html`（用 `os.path.expanduser`，跨機器/跨帳號皆可直接跑）。
  - `verify_deck.py` — 對產生好的 HTML 做幾何/文字溢出/箭頭 marker 檢查。
- `session/session.jsonl` — 這次 Claude Code 對話的原始 session 紀錄。

## 在新電腦上繼續編輯

1. 把 `build/` 底下三個腳本複製到任一工作目錄（例如 scratchpad），依序執行：
   ```
   python3 build_slides2.py   # 應輸出 "Broken arrows: 0" 與 "All links valid"
   python3 build_final.py     # 寫出 ~/Desktop/Harness 心智圖＋課程.html
   python3 verify_deck.py     # 應輸出 Errors: 0
   ```
2. 修改內容一律改 `build_slides2.py`（投影片文字、圖表）或 `diagram_lib.py`（圖表機制），改完照上面順序重跑一次，每次修改後都要重跑完整驗證。

## 接續 session

`session/session.jsonl` 是完整對話紀錄。若新電腦上的 Claude Code 專案路徑（`git clone` 到一樣的絕對路徑、一樣的使用者帳號）剛好一致，可以把這檔案放回對應的 session 儲存位置後用 `--resume` 接續；若路徑或帳號不同，session hash 對不上，接續不保證能用，但仍可以直接把這個檔案讀給新的 Claude Code session 當背景脈絡用。
