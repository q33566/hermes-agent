# Harness 拆裝手冊 —— hermes-agent 學習教材

一份 17 章的互動式教學網頁，教「LLM agent harness 是怎麼運作的」，以 hermes-agent 這個真實 repo 作為對照案例。單一自足的 `harness-course.html`，也發布成 Claude Artifact：

https://claude.ai/code/artifact/a858990b-3f99-4c02-a0bb-591e5366c06a

## 結構

- 第 1–4 章：從零設計核心概念（Harness 心智模型、最小迴圈、工具協定、context 管理與壓縮）。
- 第 5–10 章：對照 hermes-agent 原始碼講核心迴圈怎麼落地（記憶系統、狀態持久化、sub-agent 委派、provider 抽象層、語音、多程式併發）。
- 第 11–16 章：對應 hermes-agent 官方文件的 Core 分類（工具系統、Skills／Curator、LSP、記憶 provider、context files、MoA、personality／SOUL.md、plugins 等）。
- 第 17 章：Prompt 全覽——把散落在各章的提示詞模板（主系統提示、壓縮摘要、subagent 任務提示、Curator 審查、session 命名⋯）集中攤開，對照它們背後共用的輔助模型解析機制。

每章都有選擇題 quiz，可以用來自我檢查有沒有真的懂，但**不是強制關卡**——所有章節隨時可從側欄或「下一章」按鈕自由跳轉，不需要先答對才能往下走。

## 內容驗證方式

所有「hermes-agent 實際上怎麼做」的段落，都是直接讀 `.py` 原始碼（不是官方文件、不是記憶）逐條核對過的，附 file:line 出處。驗證方法：對每個章節對子（如 ch5-6、ch7-8...）派一個子 agent，要求它把課程內文跟目前這份 checkout 的原始碼逐句比對，回報任何跟原始碼不符的地方，附證據；發現的落差已經逐條修回課程內文。

已知會隨原始碼演進而過期的地方：任何寫死的行號、常數值（例如 `_MAX_TAIL_MESSAGE_FLOOR`、`nudge_interval`／`interval_hours`／`min_idle_hours` 預設值等）、檔案大小比較。之後 repo 有大改動時，建議重跑一次同樣的逐章核對流程。

## 怎麼繼續編輯

1. 編輯 `harness-course.html`（純字串拼接的 `BODY[n]` / `QUIZ[n]`，沒有建置流程）。
2. 用 `node --check` 抽出 `<script>` 內容做語法檢查。
3. 用 Playwright 跑一次全 17 章走查（含 mobile overflow 與 SVG 文字裁切檢查），確認沒有 console error。
4. 改完想同步回 Claude Artifact，就把同一個檔案重新發布到上面那個 URL。

## 更新日誌（本次 session 的工作內容）

初版（16 章、quiz 強制解鎖）建好之後，這個 session 又做了以下幾輪修訂：

**1. 全章節逐句核對原始碼（6 個子 agent 平行跑 ch5-16）**，抓到並修正的實質錯誤包括：
   - ch5：記憶快照只在「換 session」時刷新的說法不完整——compaction 中途重建 system prompt 時也會刷新。
   - ch6：`hermes_state.py`「全 repo 最大檔案」是錯的（`gateway/run.py`、`cli.py` 都更大）；DB 寫入時機從「每輪結束」修正為「一次 turn 內的多個檢查點批次寫入」。
   - ch7-8：provider API 模式漏列 `bedrock_converse`；「provider plugin 機制」的範圍講太寬（只有設定檔走 plugin，adapter 本身是寫死的固定模組）。
   - ch9-10：`AUDIO_CACHE_DIR` 不是真的環境變數；STT 內建 provider 少列了 3 個；「Level 2 做全域執行狀態檢查」應為「針對該 session」。
   - ch11-12：Docker backend 沒有唯讀 rootfs（只有 capability drop）；容器預設會跨程式重啟保留，不是「直到程式關閉」。
   - ch13-14：外部記憶 provider 數量 9→8（刪除不存在的「Memori」）；`@` context reference 其實在訊息平台也會展開，不是只在 CLI；MoA reference model 其實有一段固定顧問角色的系統提示，不是完全沒有系統提示。
   - ch15-16：system prompt 堆疊表格順序原本是錯的，已對照 `agent/system_prompt.py` 的真實組裝順序改正；`/personality` 其實是 API 呼叫時另外串接、不進快取字串，不是快取字串裡的一層。

**2. ch4 壓縮章節重新排序**：改成「先講修剪機制（含正確的 token-budget-primary + `min(protect_last_n, 8)` 下限公式）→ 再講摘要機制（含真實的 12 段式摘要模板）→ 說明 compaction = 這兩者的合稱 → 最後講兩道觸發門檻（gateway 85% 安全網 vs 主壓縮器 50%）」，取代原本先講兩道門檻的順序。

**3. 依對話中使用者提出的具體疑問，多輪追加內容**（皆已對照原始碼驗證）：
   - ch5：補上背景自我改進審查機制（`agent/background_review.py`，每 10 個使用者輪次觸發一次，fork 出限定工具白名單的 AIAgent）、澄清外部 provider 不會取代 state.db。
   - ch5 標題從「短期 vs 長期」改成跟內文一致的「自動注入 vs 隨選查詢」（原標題會誤導成 state.db 是短期，但它其實是保留最久的一份）。
   - ch6：補上 WAL／FTS5／trigram／CJK tokenizer／worktree agent／BEGIN IMMEDIATE 重試機制的白話定義；新增「session_search 是不是 RAG」的完整對比（答案：不是，是純關鍵字 FTS5+BM25，零 embedding／零向量資料庫，第 13 章部分外部 provider 才是真正的向量檢索）。
   - ch7：新增「模型只會吐文字，怎麼『生出』一個子 Agent」的逐步機制拆解（tool_call → harness 收到 parent_agent 參照 → 用同一個 AIAgent 類別重新建構 → thread pool 裡跑 run_conversation() → 結果包成 tool_result 回傳）；修正 background 預設值的說法（不是模型決定，是 harness 依委派深度強制指定）。
   - ch11：補上「誰定義可延後」（`toolsets._HERMES_CORE_TOOLS` 寫死清單）、三個橋接工具的具體參數範例、Tier 0/1/2 的具體案例（含原始碼註解裡的 Cloudflare ~3,300 工具真實案例）。
   - ch12：補上具名 skill 的三層揭露完整範例、澄清 Level 0 索引是被動烤進 system prompt（不是主動呼叫 `skills_list()`）、補上 Curator 自動觸發排程（`interval_hours` 預設 7 天、`min_idle_hours` 預設 2 小時）與「LLM 整併預設不會自動發生，需額外開 `curator.consolidate: true`」的關鍵事實。
   - ch4／ch12：統一說明「輔助模型」的三層解析鏈（任務專屬設定 → provider 的 `default_aux_model` → 主模型），指出壓縮摘要跟 Curator 用的是同一套機制。
   - ch5 → ch6：加了可點的章節內連結（`data-goto` + `.ch-link`），不用手動翻頁。

**4. Quiz 從強制關卡改成純自我檢查**：移除章節鎖定機制（`chapterState` 不再有 `locked` 狀態），所有章節可自由跳轉；quiz 文案跟著調整（提示語、通過訊息）。

**5. 新增第 17 章「Prompt 全覽」**：把主系統提示、壓縮摘要、subagent 系統提示、MoA reference/aggregator、Curator 審查、session 命名這幾份提示詞模板放進同一張表比較，並詳細拆解前面章節沒完整展開過的三份（subagent 系統提示的逐段結構、Curator 審查提示的硬性規則、session 命名的 JSON Schema + few-shot 設計）。
