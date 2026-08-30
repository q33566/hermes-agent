# Harness 拆裝手冊 —— hermes-agent 學習教材

一份 16 章的互動式教學網頁，教「LLM agent harness 是怎麼運作的」，以 hermes-agent 這個真實 repo 作為對照案例。單一自足的 `harness-course.html`（quiz 通過才能解鎖下一章），也發布成 Claude Artifact：

https://claude.ai/code/artifact/a858990b-3f99-4c02-a0bb-591e5366c06a

## 結構

- 第 1–4 章：從零設計核心概念（Harness 心智模型、最小迴圈、工具協定、context 管理與壓縮）。
- 第 5–10 章：對照 hermes-agent 原始碼講核心迴圈怎麼落地（記憶系統、狀態持久化、sub-agent 委派、provider 抽象層、語音、多程式併發）。
- 第 11–16 章：對應 hermes-agent 官方文件的 Core 分類（工具系統、Skills／Curator、LSP、記憶 provider、context files、MoA、personality／SOUL.md、plugins 等）。

每章都有選擇題 quiz，答對才能解鎖下一章。

## 內容驗證方式

所有「hermes-agent 實際上怎麼做」的段落，都是直接讀 `.py` 原始碼（不是官方文件、不是記憶）逐條核對過的，附 file:line 出處。驗證方法：對每個章節對子（如 ch5-6、ch7-8...）派一個子 agent，要求它把課程內文跟目前這份 checkout 的原始碼逐句比對，回報任何跟原始碼不符的地方，附證據；發現的落差已經逐條修回課程內文。

已知會隨原始碼演進而過期的地方：任何寫死的行號、常數值（例如 `_MAX_TAIL_MESSAGE_FLOOR`、`nudge_interval` 預設值等）、檔案大小比較。之後 repo 有大改動時，建議重跑一次同樣的逐章核對流程。

## 怎麼繼續編輯

1. 編輯 `harness-course.html`（純字串拼接的 `BODY[n]` / `QUIZ[n]`，沒有建置流程）。
2. 用 `node --check` 抽出 `<script>` 內容做語法檢查。
3. 用 Playwright 跑一次全 16 章「作答 quiz → 解鎖下一章」的走查（含 mobile overflow 與 SVG 文字裁切檢查），確認沒有 console error。
4. 改完想同步回 Claude Artifact，就把同一個檔案重新發布到上面那個 URL。
