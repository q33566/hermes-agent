# -*- coding: utf-8 -*-
import json, sys
sys.path.insert(0, '/private/tmp/claude-501/-Users-kurtshen-Projects-Research-hermes-agent/f8298acf-6e06-4b75-bff4-e4b467e8a9e7/scratchpad')
from diagram_lib import Diagram

def grid(vb, boxes, aria, cap):
    """boxes: list of (x,y,w,h,label,sub,accent)"""
    d = Diagram(vb, aria, cap)
    for b in boxes:
        x,y,w,h,label = b[0],b[1],b[2],b[3],b[4]
        sub = b[5] if len(b) > 5 else None
        accent = b[6] if len(b) > 6 else False
        d.box(x,y,w,h,label,sub,accent)
    return d.render()

# ============================================================ CORE
D = Diagram("0 0 620 320",
    "Harness 是包住模型的一層外殼：Loop 是內部邏輯，往外分派給 Tools、Memory、Context 維護等多種能力模組",
    "Loop 只是 Harness 眾多分派對象之一——工具呼叫不等於 Harness 全貌。")
D.raw('<rect x="15" y="15" width="590" height="290" fill="none" stroke="currentColor" stroke-dasharray="6 5" rx="16" opacity="0.6"/>')
D.text(40,40,"Harness",13)
D.box(230,55,160,70,"Model",accent=True)
D.box(230,160,160,50,"Loop")
D.arrow(270,160,270,125)
D.arrow(350,125,350,160)
D.box(40,250,110,40,"Tools")
D.box(170,250,110,40,"Memory")
D.box(300,250,110,40,"Context 維護")
D.box(430,250,160,40,"其他能力","Skills／Multi-Agent 等")
D.arrow(250,210,95,250)
D.arrow(283,210,225,250)
D.arrow(317,210,355,250)
D.arrow(350,210,510,250)
DIAG_HARNESS_SHELL = D.render()

# ============================================================ TOOLS
D = Diagram("0 0 460 130", "工具呼叫協定", "模型只能請求；Harness 才真正執行並回傳結果。")
D.text(60,20,"Model",11).text(360,20,"Harness",11)
D.line_plain(60,28,60,115)
D.line_plain(360,28,360,115)
D.arrow(60,48,360,48,"①請求 tool_use",75,42)
D.box(320,62,80,26,"②本地執行",accent=True)
D.arrow(360,100,60,100,"③回傳 tool_result",75,116)
DIAG_TOOLCALL = D.render()

D = Diagram("0 0 460 220", "一般做法要記得手動更新總表；hermes-agent 把註冊寫進工具本身", "少一個要記得做的步驟，就少一種會忘記的可能。")
D.text(115,18,"一般做法",12,"middle")
D.box(20,28,190,36,"工具程式碼")
D.arrow(115,64,115,88,"手動加一行",125,80)
D.box(20,88,190,36,"獨立總表 manifest")
D.arrow(115,124,115,150)
D.box(20,150,190,50,"模型可見清單","忘記加＝安靜不存在，不報錯")
D.text(345,18,"hermes-agent",12,"middle")
D.box(250,28,190,36,"工具程式碼＋register()",accent=True)
D.arrow(345,64,345,88)
D.box(250,88,190,36,"啟動：AST 掃描")
D.arrow(345,124,345,150)
D.box(250,150,190,50,"模型可見清單",accent=True)
DIAG_REGISTER = D.render()

DIAG_TOOLCATS = grid("0 0 460 150", [
  (5,5,140,42,"Web","web_search／web_extract"),
  (155,5,150,42,"Terminal＆Files","terminal／read_file／patch"),
  (315,5,140,42,"Browser","browser_navigate"),
  (5,55,140,42,"Media","vision／image／TTS"),
  (155,55,150,42,"Agent 編排","todo／delegate_task"),
  (315,55,140,42,"記憶","memory／session_search"),
  (5,105,140,42,"自動化","cronjob"),
  (155,105,150,42,"整合","MCP／Home Assistant"),
], "八大工具分類", "可依平台啟用子集（toolset），非全部常駐。")

D = Diagram("0 0 500 130", "Terminal：同介面、隔離程度遞增", "Docker 為單一長駐容器＋docker exec，非每次建立新容器。")
D.box(10,40,95,40,"local","本機直接執行")
D.box(115,40,130,40,"docker","長駐容器，權限最小化")
D.box(260,40,110,40,"ssh","遠端，無法碰原始碼")
D.box(385,40,105,40,"雲端沙箱",accent=True)
D.arrow(20,100,470,100,"隔離程度遞增",200,118)
DIAG_TERMINAL = D.render()

D = Diagram("0 0 460 175", "Tool Search 範例：先搜尋，再取得完整定義，才呼叫", "核心工具不受影響，恆常列出；此機制只延後其餘工具的細節，不影響能不能用。")
D.box(20,15,120,36,"tool_search","關鍵字找候選")
D.box(170,15,120,36,"tool_describe","換完整 schema")
D.box(320,15,120,36,"tool_call","真正呼叫",accent=True)
D.arrow(140,33,170,33).arrow(290,33,320,33)
D.text(20,72,"範例：",11)
D.text(20,90,'tool_search(queries=["create github issue", "send slack message"])',9,None,True)
D.text(20,106,"→ 命中：github.create_issue、slack.send_message",9,None,True)
D.text(20,130,'tool_describe(names=["github.create_issue"])',9,None,True)
D.text(20,146,"→ 回傳完整 JSON schema（參數、型別、必填欄位）",9,None,True)
DIAG_TOOLSEARCH = D.render()

D = Diagram("0 0 460 150", "LSP：語意層檢查在語法檢查之後", "語言伺服器缺失時靜默降級為空，絕不阻斷 write_file／patch。")
D.box(10,10,130,34,"write_file／patch")
D.arrow(75,44,75,70)
D.box(10,70,130,34,"語法檢查","ast.parse")
D.arrow(140,87,180,87,"通過",148,80)
D.box(180,70,140,34,"語言伺服器診斷",accent=True)
D.arrow(320,87,340,87)
D.box(340,60,110,54,"僅回報","本次新增的診斷")
DIAG_LSP = D.render()

# ============================================================ CONTEXT
D = Diagram("0 0 460 120", "Context 維護：兩種對策", "快取不縮減內容；壓縮才會真的變小，而且先從便宜的清除開始，才進到貴的摘要。")
D.box(20,30,180,55,"快取 caching","不縮減，只是不用重算")
D.box(260,30,180,55,"壓縮 compaction","先清除，才貴的摘要",accent=True)
DIAG_CONTEXT3 = D.render()

D = Diagram("0 0 460 110", "快取：前綴比對，一個 byte 就全毀", "穩定內容放前面、易變內容放後面，才能持續命中。")
D.box(10,30,300,40,"system prompt ＋ 工具定義（穩定前綴）",accent=True)
D.box(320,30,130,40,"易變內容")
D.arrow(300,50,320,50,"此點之後才允許變動",300,20)
D.text(160,90,"前綴任一 byte 改變 → 快取自該點起全部失效",11,"middle",True)
DIAG_CACHE = D.render()

D = Diagram("0 0 460 120", "清除：tool_use／tool_result 必須成對處理", "落單的請求會讓下一次呼叫失效，多數 API 直接拒絕。")
D.box(30,30,150,50,"tool_use")
D.box(280,30,150,50,"tool_result")
D.arrow(180,55,280,55,"配對",210,48)
D.text(230,100,"移除其一，必須同時移除／替換另一個",11,"middle",True)
DIAG_PAIR = D.render()

D = Diagram("0 0 460 130", "壓縮＝修剪＋摘要，共四步", "①②為修剪，③④為摘要；僅③真正呼叫模型。")
D.box(5,45,105,44,"①修剪","規則式，不呼叫模型")
D.box(120,45,105,44,"②劃定邊界","開頭＋近期窗口")
D.box(235,45,105,44,"③產生摘要","呼叫輔助模型",accent=True)
D.box(350,45,105,44,"④重組","開頭＋摘要＋窗口")
D.arrow(110,67,120,67).arrow(225,67,235,67).arrow(340,67,350,67)
DIAG_COMPACT4 = D.render()

D = Diagram("0 0 500 170", "壓縮觸發位置：50% 主壓縮器，85% 安全網", "數字愈大代表愈晚介入；50% 精細可調，85% 粗略保底。")
D.text(250,20,"50%",12,"middle")
D.text(250,36,"Agent 主壓縮器（可調整）",9,"middle",True)
D.arrow(250,44,250,78)
D.text(418,20,"85%",12,"middle")
D.text(418,36,"Gateway 安全網（粗估）",9,"middle",True)
D.arrow(418,44,418,78)
D.box(10,78,480,24,"")
D.text(10,118,"0%",10)
D.text(490,118,"100%",10,"end")
D.text(250,150,"context window ＜512K 時，50% 門檻自動提高到 75%",10,"middle",True)
DIAG_THRESHOLD = D.render()

# ============================================================ MEMORY
D = Diagram("0 0 460 120", "兩種「記住」完全不同", "對話歷史會被摘要清除；跨 session 記憶才是本節主題。")
D.box(10,30,200,50,"對話歷史 messages","受 context 管理影響，可被摘要／清除")
D.box(250,30,200,50,"跨 session 記憶",accent=True,)
D.text(350,72,"名稱・偏好・關鍵決策，需長期保留",9,"middle",True)
DIAG_MEM_DEF = D.render()

D = Diagram("0 0 460 130", "記憶設計取捨：兩種模型", "兩者互補，並非二選一——hermes-agent 兩者都做。")
D.box(20,15,180,46,"精選有限、自動注入","MEMORY.md／USER.md")
D.box(20,75,180,46,"完整無限、隨選查詢","state.db（session_search）")
D.arrow(200,38,340,60).arrow(200,98,340,68)
D.box(340,45,100,40,"並行運作",accent=True)
DIAG_MEMORY2 = D.render()

D = Diagram("0 0 460 210", "雙軌並行：常駐快照＋背景審查", "背景審查寫回的內容，要等下次 session（或本次觸發壓縮）才會被讀到。")
D.box(20,10,180,36,"Session 開始")
D.arrow(110,46,110,70)
D.box(20,70,180,40,"讀入 MEMORY.md／USER.md","一次性快照，寫入 system prompt")
D.box(260,10,180,36,"使用者輪次計數 = 10")
D.arrow(350,46,350,70)
D.box(260,70,180,40,"fork 審查子 Agent","工具白名單限縮，不碰主對話快取",accent=True)
D.arrow(350,110,240,150,"寫回",270,135)
D.box(20,150,420,45,"寫回 MEMORY.md／USER.md","跟左側同一組檔案（各自獨立），下次 session（或本次壓縮）才生效",accent=True)
DIAG_MEM_DUAL = D.render()

D = Diagram("0 0 460 170", "state.db：單一 SQLite，WAL 模式仲裁多寫入者", "短逾時快速失敗＋隨機退避重試＋BEGIN IMMEDIATE 搶鎖。")
D.box(10,10,110,34,"CLI").box(175,10,110,34,"Gateway").box(340,10,110,34,"worktree agent")
D.arrow(65,44,230,90).arrow(230,44,230,90).arrow(395,44,230,90)
D.box(160,90,140,50,"state.db（WAL）",accent=True)
D.text(230,155,"每 50 次寫入做一次 checkpoint，合併日誌回主檔案",10,"middle",True)
DIAG_STATEDB = D.render()

D = Diagram("0 0 460 150", "session_search：搜尋過去對話紀錄的關鍵字檢索", "零 embedding、零向量資料庫；模型主動呼叫才觸發，非自動注入。")
D.box(20,20,150,36,"查詢字串")
D.arrow(170,38,220,38)
D.box(220,20,110,36,"FTS5 索引")
D.arrow(330,38,360,38)
D.box(360,20,90,36,"BM25 排序",accent=True)
D.box(20,90,430,40,"對照組（非本機制）：embedding → 向量資料庫 → 相似度搜尋")
DIAG_SEARCH = D.render()

D = Diagram("0 0 460 140", "外部記憶 Provider：疊加，不取代", "啟用後三層同時運作，不會停用內建機制。")
D.box(20,10,180,32,"MEMORY.md／USER.md")
D.box(20,49,180,32,"state.db")
D.box(20,88,180,32,"外部 provider（8 選 1）",accent=True)
D.arrow(200,26,300,58).arrow(200,65,300,68).arrow(200,104,300,78)
D.box(300,38,150,58,"同時餵入","system prompt／context")
DIAG_EXTMEM = D.render()

# ============================================================ SKILLS
D = Diagram("0 0 460 140", "用內容形態判斷該存 Memory 還是 Skill", "一句話講得完 → Memory；需要走多步驟操作 → Skill。")
D.box(20,15,190,50,"Memory","小而持久的事實")
D.box(250,15,190,50,"Skill","長而完整的流程",accent=True)
D.text(230,100,"判準：一句話 → Memory；多步驟流程 → Skill",11,"middle",True)
DIAG_SKILL_DEF = D.render()

D = Diagram("0 0 460 150", "Skills 三層漸進式揭露", "Level 0 為常駐成本；Level 1／2 為按需成本，非全部載入。")
D.box(20,20,130,42,"Level 0 索引","名稱／描述／分類")
D.box(20,80,130,42,"Level 1 完整內容","skill_view(name)")
D.box(290,80,150,42,"Level 2 參考檔案","file_path 指定",accent=True)
D.arrow(85,62,85,80).arrow(150,101,290,101)
DIAG_SKILLS3 = D.render()

D = Diagram("0 0 460 130", "Skill 儲存三層優先權", "優先權與信任度成反比：Project 最高權卻最不受信任。")
D.box(20,10,300,32,"Project","優先權最高、最不受信任，需明確授權")
D.box(20,49,300,32,"Local","背景 Curator 唯一可自動寫入層級")
D.box(20,88,300,32,"External","設定檔指定的額外目錄")
DIAG_SKILL_TIERS = D.render()

D = Diagram("0 0 460 130", "Skills Hub：安裝前統一安全掃描", "danger 等級掃描結果無法強制覆蓋。")
D.box(10,10,100,34,"bundled","永遠信任")
D.box(120,10,100,34,"official")
D.box(230,10,100,34,"trusted")
D.box(340,10,110,34,"community")
D.arrow(230,44,230,80)
D.box(140,80,180,36,"安裝前安全掃描",accent=True)
DIAG_HUB = D.render()

D = Diagram("0 0 460 170", "Curator：免費自動轉換 vs 付費 LLM 整併", "兩條件同時滿足才觸發檢查：距上次 > 7 天 且 閒置 > 2 小時。")
D.box(10,15,200,40,"閒置 30 天 → stale","規則式，無 LLM 呼叫")
D.box(10,63,200,40,"閒置 90 天 → archived","可還原，從不真刪")
D.box(250,15,200,88,"LLM 整併（預設關閉）","50–100 次輔助模型呼叫／次",accent=True)
DIAG_CURATOR = D.render()

D = Diagram("0 0 460 120", "Plugin 權限：宣告＋一次性確認，非沙箱", "同進程執行；只安裝信任來源才是真正防線。")
D.box(10,35,140,40,"Plugin manifest","宣告所需權限")
D.arrow(150,55,220,55)
D.box(220,35,120,40,"使用者一次性確認")
D.arrow(340,55,370,55)
D.box(370,35,80,40,"授權生效",accent=True)
DIAG_PLUGIN_CONSENT = D.render()

# ============================================================ MULTI-AGENT
D = Diagram("0 0 460 150", "委派：子 Agent 於獨立 context 執行", "父層僅收到最終結構化摘要，不接觸完整過程。")
D.box(20,45,120,55,"父 Agent")
D.box(320,45,120,55,"子 Agent","獨立 context",accent=True)
D.arrow(140,62,320,62,"delegate_task(goal, context)",150,54)
D.arrow(320,85,140,85,"回傳結構化摘要",150,112)
DIAG_DELEGATE = D.render()

D = Diagram("0 0 460 130", "委派 vs MoA：切開工作 vs 問過多個意見", "委派是切開工作、各自獨立跑；MoA 是同一份工作、問過多個意見、只有一人動手。")
D.box(20,25,190,80,"委派 delegation","切開工作，各自獨立 context 跑")
D.box(250,25,190,80,"Mixture of Agents","同一份工作，多個意見後一人動手",accent=True)
DIAG_MA_OVERVIEW = D.render()

D = Diagram("0 0 460 150", "Subagents Know Nothing：邊界即設計", "唯一例外：工作目錄下的 AGENTS.md 會被嵌入子 Agent 系統提示。")
D.box(10,10,150,34,"父層對話歷史")
D.raw('<line x1="35" y1="44" x2="135" y2="90" stroke="currentColor" stroke-width="1.4"/><line x1="135" y1="44" x2="35" y2="90" stroke="currentColor" stroke-width="1.4"/>')
D.text(85,71,"不傳遞",10,"middle",True)
D.box(10,90,150,34,"goal ／ context 字串",accent=True)
D.arrow(160,107,300,107)
D.box(10,130,150,20,"（例外）AGENTS.md")
D.arrow(160,140,300,140)
D.box(300,60,150,90,"子 Agent 系統提示")
DIAG_KNOWNOTHING = D.render()

D = Diagram("0 0 460 130", "子 Agent＝同一 AIAgent 類別的另一個實例", "跑在同進程的另一條執行緒，非另開行程。")
D.box(150,10,160,34,"AIAgent 類別",accent=True)
D.arrow(200,44,80,80).arrow(280,44,380,80)
D.box(10,80,150,40,"父 Agent 實例","主執行緒")
D.box(300,80,150,40,"子 Agent 實例","thread pool 執行緒")
DIAG_SAMECLASS = D.render()

D = Diagram("0 0 500 130", "background 由深度強制決定，非模型自選", "頂層委派恆為背景；orchestrator 再往下委派恆為同步。")
D.box(10,10,220,40,"depth = 0（頂層呼叫）")
D.arrow(120,50,120,80,"強制",100,68)
D.box(10,80,220,36,"background = True",accent=True)
D.box(270,10,220,40,"depth ＞ 0（orchestrator 委派）")
D.arrow(380,50,380,80,"強制",360,68)
D.box(270,80,220,36,"background = False",accent=True)
DIAG_DEPTH = D.render()

D = Diagram("0 0 460 170", "MoA：Reference 產出分析，Aggregator 唯一動手", "Reference 無工具權限；真正呼叫工具的只有 Aggregator。")
D.box(20,15,140,44,"Reference A","無工具權限")
D.box(20,71,140,44,"Reference B","無工具權限")
D.box(260,45,150,60,"Aggregator",accent=True,)
D.arrow(160,37,260,68).arrow(160,93,260,88)
D.box(310,120,130,36,"呼叫工具","標準協定")
D.arrow(335,105,335,120)
DIAG_MOA = D.render()

DIAG_ROLES = grid("0 0 460 110", [
  (10,10,210,80,"Reference（顧問）","輕量・無工具・固定角色提示・僅產出分析"),
  (240,10,210,80,"Aggregator（執行者）","接收全部分析為參考・唯一呼叫工具者",None,True),
], "顧問與執行者：分工不對稱", "分工不對稱，成本可控在顧問這一側。")

D = Diagram("0 0 460 130", "顧問分析附加於快取邊界之後", "位置決定成敗：附加在已快取內容之後才不觸發快取失效。")
D.box(10,45,260,40,"system prompt ＋ 對話歷史（已快取）",accent=True)
D.box(280,45,170,40,"這輪使用者訊息 ＋ 顧問分析")
D.arrow(270,65,280,65,"附加於此",240,90)
DIAG_MOACACHE = D.render()

D = Diagram("0 0 460 100", "成本旋鈕：顧問重跑頻率三檔", "延遲與花費隨重跑頻率遞增，user_turn 為預設最省模式。")
D.box(10,30,130,40,"user_turn","每回合一次（預設）")
D.box(165,30,130,40,"every_n:N","折衷")
D.box(320,30,130,40,"per_iteration","每次工具呼叫皆重跑",accent=True)
D.arrow(20,85,440,85,"成本遞增",190,100)
DIAG_FANOUT = D.render()

# ============================================================ IDENTITY
D = Diagram("0 0 460 180", "三入口先各自對接不同真實系統，介接完成才收斂進核心迴圈", "介接完成後，後續處理與入口來源無關。")
D.box(10,10,190,34,"CLI","讀 stdin／寫 stdout")
D.box(10,58,190,34,"訊息平台 Gateway","對接平台 API")
D.box(10,106,190,34,"排程 Cron","無即時輸入，由排程觸發")
D.arrow(200,27,280,60).arrow(200,75,280,70).arrow(200,123,280,80)
D.box(280,45,170,50,"核心迴圈",accent=True)
DIAG_ENTRY3 = D.render()

D = Diagram("0 0 460 110", "語音輸入管線：STT 為前處理，非模型直接處理", "模型自始至終只接收文字。")
D.box(10,30,90,45,"接收音檔")
D.box(130,30,90,45,"STT 轉文字",accent=True)
D.box(250,30,90,45,"併入訊息")
D.box(370,30,80,45,"Loop")
D.arrow(100,52,130,52).arrow(220,52,250,52).arrow(340,52,370,52)
DIAG_VOICE = D.render()

D = Diagram("0 0 460 150", "Gateway 雙層防護，各管一種競態", "Level1 防同會話重複處理；Level2 讓控制指令插隊生效。")
D.box(160,10,140,32,"訊息進入")
D.arrow(230,42,230,70)
D.box(30,70,180,40,"Level 1：平台層","擋同對話重複並行訊息")
D.arrow(120,110,120,130,"通過",130,122)
D.box(250,70,180,40,"Level 2：Runner 層","攔截 /stop 等控制指令，session 範圍",accent=True)
DIAG_GATEWAY2L = D.render()

D = Diagram("0 0 460 110", "專案情境檔：第一個命中者勝出", ".hermes.md → AGENTS.md → CLAUDE.md → .cursorrules，SOUL.md 為獨立另一條路徑。")
D.box(10,10,90,34,".hermes.md",accent=True)
D.box(120,10,90,34,"AGENTS.md")
D.box(230,10,90,34,"CLAUDE.md")
D.box(340,10,110,34,".cursorrules")
D.arrow(100,27,120,27).arrow(210,27,230,27).arrow(320,27,340,27)
D.box(150,65,160,32,"SOUL.md（獨立於此鏈）")
DIAG_CTXFILES = D.render()

D = Diagram("0 0 460 100", "SOUL.md：只認 HERMES_HOME，不認專案目錄", "刻意設計：身份跟隨實例，不隨你在哪個資料夾啟動而改變。")
D.box(20,30,180,40,"HERMES_HOME",accent=True)
D.arrow(200,50,300,50)
D.box(300,30,140,40,"System Prompt")
D.text(110,90,"（當前專案目錄：不會被讀取）",9,"middle",True)
DIAG_SOUL = D.render()

D = Diagram("0 0 460 150", "AGENTS.md：從專案根目錄到你所在的資料夾，逐層合併", "子目錄採漸進式發現：實際存取時才載入，維持快取穩定。")
D.box(10,40,90,40,"git root","專案最上層")
D.box(130,40,90,40,"子目錄 A")
D.box(250,40,90,40,"子目錄 B")
D.box(370,40,80,40,"cwd","你所在的資料夾",accent=True)
D.arrow(100,60,130,60).arrow(220,60,250,60).arrow(340,60,370,60)
D.arrow(20,105,450,105,"合併順序：越後面＝越具體＝優先權越高",115,122)
DIAG_AGENTSMD = D.render()

D = Diagram("0 0 460 115", "手動注入內容的配額：25% 警告，50% 拒絕", "CLI 與訊息平台皆適用同一套配額限制。")
D.box(10,20,440,20,"展開內容占 context 長度 0% ──────────────── 100%")
D.arrow(120,40,120,70,"25%：警告仍展開",70,90)
D.arrow(240,40,240,70,"50%：拒絕展開",190,90)
DIAG_ATQUOTA = D.render()

DIAG_ORTHO = grid("0 0 460 100", [
  (10,10,210,80,"Skin","CLI 視覺呈現：配色、動畫"),
  (240,10,210,80,"SOUL.md／Personality","語氣、身份",None,True),
], "外觀與人格：兩條互不影響的獨立軸", "換 skin 不影響語氣；換 personality 不影響配色。")

DIAG_MDTABLE = (
  '<div class="diagram"><figure><table>'
  '<tr><th>檔案</th><th>範圍</th><th>誰更新</th><th>怎麼被讀取</th></tr>'
  '<tr><td>MEMORY.md／USER.md</td><td>HERMES_HOME<br>跨專案共用</td>'
  '<td>agent 背景自動寫回<br>不需下指令</td><td>session 開始載入一次<br>成為穩定快照</td></tr>'
  '<tr><td>SOUL.md</td><td>HERMES_HOME<br>跨專案共用</td>'
  '<td>使用者手動編輯<br>或首次啟動填預設值——agent 自己從不改</td><td>session 開始載入一次<br>system prompt 第一層</td></tr>'
  '<tr><td>AGENTS.md</td><td>專案目錄<br>沿路徑鏈式合併</td>'
  '<td>agent 執行 /init 才會寫<br>其餘時候唯讀</td><td>沿 git root 到工作目錄逐層載入<br>＋漸進式子目錄發現</td></tr>'
  '</table><figcaption>四份 md 檔案，範圍、誰更新、怎麼被讀取都不一樣——別被「都是 md」騙了。</figcaption></figure></div>'
)

# ============================================================ GUIDANCE
DIAG_PROMPTS_MANY = grid("0 0 460 130", [
  (10,10,140,50,"主系統提示","唯一使用者看得見",None,True),
  (160,10,140,50,"壓縮摘要","背景任務"),
  (310,10,140,50,"Subagent 提示","背景任務"),
  (85,70,140,50,"Curator 審查","背景任務"),
  (235,70,140,50,"Session 命名","背景任務"),
], "五套提示詞模板中，只有一套是使用者看得見的", "其餘四套皆為背景任務，模型與使用者都感知不到。")

D = Diagram("0 0 460 200", "System Prompt 八層堆疊：僅第⑧層不進快取", "①–⑦整體快取；⑧每次呼叫獨立串接。")
_labels = ['① SOUL.md','② 工具／模型 guidance','③ 平台線索','④ AGENTS.md（專案情境）',
           '⑤ Skills 索引','⑥ MEMORY.md／USER.md（記憶／使用者情境）','⑦ 時間戳','⑧ /personality（不進快取）']
for i,t in enumerate(_labels):
    D.box(30,8+i*22,400,18,t, accent=(i==7))
DIAG_PROMPTSTACK = D.render()

D = Diagram("0 0 500 130", "背景任務共用同一輔助模型解析鏈", "壓縮、Curator、MoA、Session 命名皆走同一條解析路徑，只換任務名稱。")
D.box(10,45,140,40,"任務專屬設定")
D.arrow(150,65,180,65)
D.box(180,45,170,40,"provider 預設輔助模型")
D.arrow(350,65,380,65)
D.box(380,45,110,40,"主模型",accent=True)
D.text(250,105,"壓縮／Curator／MoA／命名 共用此鏈，僅任務名稱不同",10,"middle",True)
DIAG_AUXCHAIN = D.render()

D = Diagram("0 0 460 130", "設計原則：風險越高，規則越死", "低風險任務保留模型自主判斷空間，高風險任務逐條約束邊界。")
D.box(10,30,200,34,"Session 命名","低風險 → 規則寬鬆")
D.box(250,30,200,34,"Curator 審查","高風險 → 規則詳盡",accent=True)
D.arrow(20,80,440,80,"風險程度遞增 → 規則具體程度遞增",130,95)
DIAG_RISKRULE = D.render()

D = Diagram("0 0 460 110", "結構化輸出排除「回答問題」失敗模式", "json_schema 從格式上就約束住輸出，不靠模型自律。")
D.box(10,30,200,50,"自由文字生成","可能誤判為回答使用者問題")
D.box(250,30,200,50,"json_schema 強制格式",accent=True,)
D.text(350,72,'{"title": "..."}',10,"middle",True)
DIAG_STRUCTOUT = D.render()

DIAG_RECAP = grid("0 0 460 190", [
  (10,10,140,55,"Tools","不會動手→行動力"),
  (160,10,140,55,"Multi-Agent","context 塞爆／需平行"),
  (310,10,140,55,"Identity","不知道自己是誰→身份設定"),
  (10,75,140,55,"Skills","不懂特定流程→補上"),
  (160,75,140,55,"Memory","不會記得→跨session"),
  (310,75,140,55,"Guidance/Prompts","不知怎麼用好前五者",True),
  (10,145,440,35,"Context 維護貫穿全部六者，不是第七個節點",None,True),
], "六個節點各補模型一種天生缺口", "同一套問題，換了場景就會逼出不同答案——這正是你能自己動手設計的地方。")

DIAG_MOTIVATION = grid("0 0 460 120", [
  (20,20,190,80,"無法行動","API 只回傳文字，不會真的動手"),
  (250,20,190,80,"無法記憶","每次呼叫都是全新請求，不記得上一句"),
], "模型 API 天生缺兩種能力", "這兩個缺口，決定了接下來所有模組存在的理由。")

DIAG_AGENDA = grid("0 0 460 190", [
  (10,10,140,55,"Tools","不會動手→行動力"),
  (160,10,140,55,"Multi-Agent","context 塞爆／需平行"),
  (310,10,140,55,"Identity","不知道自己是誰→身份設定"),
  (10,75,140,55,"Skills","不懂特定流程→補上"),
  (160,75,140,55,"Memory","不會記得→跨session"),
  (310,75,140,55,"Guidance/Prompts","不知怎麼用好前五者",True),
  (10,145,440,35,"Context 維護貫穿全部六者，不是第七個節點",None,True),
], "接下來依序講完六個模組", "每個模組補上模型的一種天生缺口，Context 維護貫穿全部。")

# ============================================================ CLUSTERS & SLIDES
CLUSTERS = [
  {"id":"cover","label":"封面","gap":"","angle":None,"chapters":[]},
  {"id":"intro","label":"開場","gap":"從問題到解法","angle":None,"chapters":[]},
  {"id":"core","label":"核心迴圈","gap":"起點：模型只會推理，其餘都要補上","angle":None,"chapters":["CH.01","CH.02","CH.10"]},
  {"id":"tools","label":"Tools","gap":"模型不會動手 → 補上行動力","angle":0,"chapters":["CH.03","CH.08","CH.11","CH.16"]},
  {"id":"context","label":"Context 維護","gap":"補上能力的代價：內容會塞爆，六節共用同一套收斂機制","angle":None,"chapters":["CH.04"]},
  {"id":"memory","label":"Memory","gap":"模型不會記得 → 補上跨 session 記憶","angle":240,"chapters":["CH.05","CH.06","CH.13"]},
  {"id":"skills","label":"Skills","gap":"模型不懂你的特定流程 → 補上","angle":180,"chapters":["CH.12","CH.15"]},
  {"id":"multiagent","label":"Multi-Agent","gap":"單一 Agent 難平行、context 易塞爆 → 委派其他 agent","angle":120,"chapters":["CH.07","CH.14"]},
  {"id":"identity","label":"Identity","gap":"模型不知道自己是誰、該守哪些規則 → 補上身份與情境設定","angle":60,"chapters":["CH.09","CH.13","CH.15"]},
  {"id":"guidance","label":"Guidance／Prompts","gap":"模型不知道怎麼用好前五者 → 補上引導","angle":300,"chapters":["CH.15","CH.17"]},
]

def S(id_, title, bullets, diagram=None, links=None, src=None, impl=None, cover=False, subtitle=None):
    return {"id":id_, "title":title, "bullets":bullets, "diagram":diagram or "", "links":links or [],
            "src":src or "", "impl":impl or [], "cover":cover, "subtitle":subtitle or ""}

SLIDES = {
"cover": [
  S("cover-1","LLM Agent Harness 拆解",
    [],
    cover=True,
    subtitle="從模型的天生限制，推導出完整的 harness 設計——以 hermes-agent 為實作案例"),
],
"intro": [
  S("intro-1","模型的限制",
    ["呼叫模型 API 叫它「讀這個檔案、改完存檔」——它只會回一段文字說要怎麼做，檔案不會真的被讀到或改到。",
     "每次呼叫都是全新、獨立的請求——不重送歷史，它不會知道上一句說了什麼。",
     "這兩個缺口，決定了接下來所有模組存在的理由。"],
    DIAG_MOTIVATION),
  S("intro-2","解法總覽",
    ["Tools（補行動力）→ Context 維護（貫穿全部）→ Memory（補跨 session）→ Skills（補特定流程）→ Multi-Agent（補平行與 context 過載）→ Identity（補身份與情境設定）→ Guidance/Prompts（補怎麼用好前五者）。",
     "每個模組都是同一個問題的答案：模型缺哪種能力，就用對應機制補上——同一套推理方式，可套用在任何 harness 的設計上。"],
    DIAG_AGENDA),
],
"core": [
  S("core-1","什麼是 Harness",
    ["模型 API 無狀態，且只能輸出文字——不會記得歷史，也不會真的動手。",
     "迴圈補上這個缺口：組裝歷史 → 呼叫模型 → 執行工具 → 結果併入歷史 → 循環。",
     "接下來六節，依序補上模型還缺的每一種能力：Tools、Context 維護、Memory、Skills、Multi-Agent、Identity、Guidance/Prompts。"],
    DIAG_HARNESS_SHELL, links=[("tools-1","下一節：Tools 呼叫協定")], src="CH.01／CH.02",
    impl=["業界沒有統一官方命名：常見說法是 agent loop，或沿用學術上的 ReAct 框架（Yao et al., 2022）；hermes-agent 內部函式為 run_conversation()（agent/conversation_loop.py），原始碼註解稱之為「the agent conversation loop」，同樣沒有專屬品牌名稱。",
          "接上工具後，assistant 端內容永遠是「區塊陣列」（text／tool_use 混合），不是純字串。"]),
],
"tools": [
  S("tools-1","呼叫協定",
    ["模型只能請求呼叫工具，執行永遠由 Harness 負責——工具定義是一份 JSON schema，模型看到後最多只能說「我想用這個」。",
     "平行呼叫要合併回傳：模型一次可能請求多個工具，全部執行完才合併成單一訊息送回；失敗附加 is_error: true，不能靜默丟棄。",
     "執行前先做風險分級：唯讀查詢直接放行；有副作用操作標記確認；破壞性操作預設要求人工核准。"],
    DIAG_TOOLCALL, src="CH.03",
    impl=["stop_reason 除了 tool_use／end_turn，還有 max_tokens（回應被截斷，可能含未寫完的 tool_use，不能照做）。",
          "此處命名（tool_use／tool_result）是 Anthropic Messages API 的形狀；其他供應商可能用獨立的 tool 角色＋tool_calls 欄位承載同樣資訊。",
          "hermes-agent 用執行緒池同時發動多個工具呼叫，結果依模型原呼叫順序重新排列後才回傳。",
          "風險比對是一組已知危險模式的規則列表，不是模型自行判斷；命中就先卡住，不直接執行——例如危險 shell 指令。"]),
  S("tools-5","分類與啟用",
    ["八大類：Web／Terminal＆Files／Browser／Media／Agent 編排／記憶／自動化／整合，各自補一種行動缺口。",
     "工具裝多了會直接吃掉 context：不是全部常駐，可以依場景只啟用需要的分類——但就算只開必要分類，數量還是可能多到成為問題，這是下一頁 Tool Search 要處理的事。"],
    DIAG_TOOLCATS, src="CH.11",
    impl=["分類定義在 toolsets.py，可用 `hermes chat --toolsets \"web,terminal\"` 或互動式的 `hermes tools` 指定啟用哪些分類。",
          "核心工具清單（terminal／read_file／memory 等）寫死在 toolsets._HERMES_CORE_TOOLS，不受平台開關影響。"]),
  S("tools-7","Tool Search",
    ["假設你有 3,300 個工具，光是完整列出清單就要吃掉約 32K token（模型讀寫文字的計量單位），還沒開始做事就先塞爆一大塊 context。",
     "三段式：tool_search → tool_describe → tool_call；核心工具不受影響，恆常列出。"],
    DIAG_TOOLSEARCH, links=[("skills-2","同一設計模式：Skills")], src="CH.11",
    impl=["預算公式：min(listing_max_tokens=4000, context 視窗 × 5%)，兩者皆可調整。",
          "核心工具豁免清單寫死在 toolsets._HERMES_CORE_TOOLS，不受此機制影響。"]),
  S("tools-8","LSP（Language Server Protocol）",
    ["write_file／patch 後，先語法檢查，通過才做語意檢查——抓叫錯函式、型別不合這類語法合法但邏輯錯的問題。",
     "只回報本次編輯新增的診斷；語言伺服器缺失時靜默降級，不阻斷寫入。"],
    DIAG_LSP, src="CH.16",
    impl=["語言伺服器閒置 600 秒（預設）自動關閉釋放資源，下次用到時懶啟動（lazy-spawn）重開。",
          "僅在偵測到 git repo 時才啟動；診斷比對「編輯前基準線」與「編輯後結果」，只留新增的部分。"]),
  S("tools-closing","小結",
    ["工具定義、風險規則、Tool Search 的候選清單……全部都要送進模型看得到的那段文字裡，而這段文字不會自動變小。",
     "下一節要處理的，就是這個代價本身：內容一直塞，最後會發生什麼事？"],
    src="CH.11"),
],
"context": [
  S("context-1","總覽",
    ["成因：模型無狀態（見核心迴圈），每輪需重送完整歷史，文字量只會愈滾愈大，不會自己變小。",
     "「Context」（context window）就是模型一次能讀進去的文字上限；快取（caching）不縮減內容，壓縮（compaction）才會真的變小——而壓縮本身是先便宜清除、才貴的摘要，不是兩個可以分開開的獨立策略。"],
    DIAG_CONTEXT3, src="CH.04"),
  S("context-2","快取",
    ["穩定內容（system prompt——送給模型的角色設定與規則文字——跟工具定義）放前面，易變內容放後面才能持續命中。"],
    DIAG_CACHE, links=[("identity-6","應用案例：AGENTS.md 漸進式發現")],
    src="CH.04",
    impl=["hermes-agent 對 Anthropic 模型的快取邊界策略：system prompt ＋最近 3 則訊息的滾動視窗，最多 4 個快取斷點，可選 5 分鐘或 1 小時存留時間。"]),
  S("context-4","壓縮",
    ["修剪（trimming）：規則式移除窗口外舊工具結果，開頭固定訊息永不變動——移除時 tool_use／tool_result 必須成對處理，落單會讓下一次呼叫直接失效。",
     "摘要（summarization）：另外呼叫一個較小、較便宜的模型，依固定模板產出結構化摘要，憑證一律遮罩為 [REDACTED]。",
     "二次以後為疊代式：新摘要完整取代舊摘要，非拼接。"],
    DIAG_COMPACT4, links=[("guidance-3","這個輔助模型怎麼被選出來：Guidance/Prompts")], src="CH.04",
    impl=["修剪公式：tail_token_budget = clamp(context×2.5%, 10000, 25000)；訊息筆數下限 min(protect_last_n, 8)；開頭固定 protect_first_n=3 則永不動。",
          "重新組裝歷史時，hermes-agent 會主動清掉任何因切割而落單的工具呼叫配對，確保不會產生無效請求。",
          "摘要 token 預算：max(2000, min(內容 token×20%, min(context×5%, 10000)))。",
          "模板段落含 Goal／Constraints &amp; Preferences／Completed Actions／Active State／Blocked／Key Decisions／Errors &amp; Fixes／Relevant Files／Critical Context 等固定欄位。"]),
  S("context-5","觸發門檻",
    ["Gateway 安全網 85%（粗估字元數）；Agent 主壓縮器 50%（真實 token 數，可調整）。",
     "小結：快取／壓縮處理的是「內容多到塞不下」；但有些事情你會想要它刻意留很久、跨越好幾次對話都還在——這是下一節 Memory 的主題。"],
    DIAG_THRESHOLD, src="CH.04",
    impl=["Gateway 端常數位於 gateway/run.py；Agent 端 512K／75% 門檻常數位於 agent/context_compressor.py。"]),
],
"memory": [
  S("memory-1","兩種記憶",
    ["對話歷史：受 context 管理影響，可被摘要或清除——這是上一節的範圍。",
     "跨 session 記憶：本節主題，指需長期保留的名稱、偏好、關鍵決策，就算歷史被清掉也不能丟。"],
    DIAG_MEM_DEF, src="CH.05"),
  S("memory-3","MEMORY.md／USER.md",
    ["兩份獨立檔案：MEMORY.md（agent 自己的筆記）與 USER.md（關於使用者的側寫）——各自容量小、有字元數上限（非 token），每輪自動注入 system prompt。",
     "怎麼被使用：session 啟動時載入一次，之後整個 session 期間是穩定快照（snapshot），不會中途重讀。",
     "怎麼被更新：不需要使用者下指令——累積一定輪次後，agent 自己觸發背景審查，寫回這兩份檔案。"],
    DIAG_MEM_DUAL, links=[("skills-5","同類機制：Skills 的 Curator"),("multiagent-1","背景程序的實作原理：Multi-Agent")], src="CH.05",
    impl=["實際上限：MEMORY.md 約 2,200 字元、USER.md 約 1,375 字元（字元數硬限制，非 token）。",
          "memory 工具只有 add／replace／remove 三種操作，以子字串比對，沒有 read 動作。",
          "審查觸發門檻：memory.nudge_interval 預設 10 個使用者輪次；這個背景程序其實是 fork 出的一個工具白名單（whitelist）限縮的子 Agent，完全不碰主對話的 prompt 快取。"]),
  S("memory-4","state.db",
    ["完整對話歷史存在單一 SQLite 資料庫 state.db，CLI／Gateway／worktree agent 共用同一份。",
     "怎麼被更新：多個程式同時寫同一份檔案——短逾時快速失敗＋隨機退避重試＋搶鎖機制；每 50 次寫入做一次 checkpoint。",
     "怎麼被查找：session_search 用 FTS5 全文索引 ＋ BM25 排序，零 embedding、零向量資料庫——模型主動呼叫才觸發，不是自動注入。"],
    DIAG_STATEDB, src="CH.06",
    impl=["連線逾時 1 秒；重試退避 20–150ms，爭用愈久拉高到 250ms–1s；一般寫入時間預算 20 秒，逐字稿等關鍵寫入放寬到 60 秒。",
          "批次寫入函式 SessionDB.append_messages_batch()，一次 turn 內多個檢查點觸發，不等到 session 結束才存檔。",
          "三張不同拆字法（tokenizer）的 FTS 表：messages_fts（空白分詞）／_fts_trigram（三字元重疊切法）／_fts_cjk（中日韓專用）。",
          "語意檢索（非關鍵字）由部分外部 provider 另外提供，session_search 本身零向量資料庫。"]),
  S("memory-6","外部 Provider",
    ["8 種可選 provider，同時僅能啟用一個；啟用後 MEMORY.md／USER.md／state.db 全部照常運作，並非替代關係。",
     "小結：記憶解決的是「記得事實」；但模型不只需要記得事，還需要知道「這件事具體怎麼做」——這是下一節 Skills 的主題。"],
    DIAG_EXTMEM, src="CH.13",
    impl=["8 種內建 provider：Honcho／OpenViking／Mem0／Hindsight／Holographic／RetainDB／ByteRover／Supermemory（plugins/memory/ 目錄）。"]),
],
"skills": [
  S("skills-1","Memory vs Skill",
    ["一句話講得完的事實 → Memory；需要走多步驟操作的流程 → Skill。",
     "記憶：小而持久。Skill：長而完整，可以很龐大而不昂貴。"],
    DIAG_SKILL_DEF, src="CH.12",
    impl=["Skill 落地為一份 SKILL.md（核心心智模型＋索引），大型 skill 可搭配 references/ 底下的細節檔案。"]),
  S("skills-2","三層揭露",
    ["Level 0：索引常駐 system prompt。Level 1：取得完整內容。",
     "Level 2：取得特定參考檔案，僅在需要細節時載入。"],
    DIAG_SKILLS3, links=[("tools-7","同一設計模式：Tools 的 Tool Search")], src="CH.12",
    impl=["對應函式：skill_view(name) 取 Level 1；skill_view(name, file_path=...) 取 Level 2（tools/skills_tool.py）。",
          "Level 0 索引是被動烤進 system prompt，不是靠模型主動呼叫 skills_list() 才出現。"]),
  S("skills-3","儲存優先權",
    ["Project：優先權最高、信任度最低，需明確授權，每次載入強制安檢。",
     "Local：背景 Curator 唯一可自動寫入層級；使用者可直接請 agent 修改任何來源的 skill。"],
    DIAG_SKILL_TIERS, src="CH.12",
    impl=["Project 層需要使用者明確執行 `hermes skills trust` 授權才會被信任並載入。"]),
  S("skills-4","Skills Hub",
    ["信任等級：bundled／official／trusted／community 依序遞減。",
     "danger 等級掃描結果無法用 --force 強制覆蓋。"],
    DIAG_HUB, src="CH.12"),
  S("skills-5","Curator",
    ["自動轉換：零 LLM 呼叫，純規則式——每個 skill 閒置 30 天 → stale，90 天 → archived（可還原，從不真刪）。",
     "LLM 整併：預設關閉，需額外設定 curator.consolidate: true 才會跑——單次審查約 50–100 次輔助模型呼叫。",
     "兩者共同前提：Curator 本身要先被觸發——距上次執行 > 7 天（interval_hours 預設 168 小時），且機器閒置 > 2 小時（min_idle_hours），才會在 CLI／Gateway 啟動時檢查一次。"],
    DIAG_CURATOR, links=[("memory-3","同類機制：Memory 的背景自我審查")], src="CH.12"),
  S("skills-6","Plugin",
    ["四種類型：一般 plugin／記憶 provider／context engine／model provider，都是程式碼層擴充，不是知識文件。",
     "第三方 plugin 預設全部停用，提權需在 manifest 宣告並取得一次性使用者確認——這是同意層，不是沙箱，信任來源才是真防線。",
     "小結：到這裡，單一 Agent 能補的能力已經差不多了；但有些任務單一 Agent 天生做不完——這是下一節 Multi-Agent 的主題。"],
    DIAG_PLUGIN_CONSENT, src="CH.15",
    impl=["記憶 provider 與 context engine 屬於「exclusive」類型：同時只能有一個生效。"]),
],
"multiagent": [
  S("multiagent-0","兩種機制",
    ["委派（delegation）：把工作切開，分給獨立的子 Agent 各自完成——每個子 Agent 有自己完整、跟父層隔離的 context 跟工具權限，等於另開一個完整的迷你任務。",
     "Mixture of Agents（MoA）：不是另開 agent，是同一輪對話裡先問過幾個模型的意見（這些「顧問」沒有自己的 context、沒有工具權限，只是看一眼同一份對話），最後由唯一一個 Aggregator 綜合意見、真正動手。",
     "接下來先講委派，最後講 MoA。"],
    DIAG_MA_OVERVIEW),
  S("multiagent-1","委派動機",
    ["兩種情況該委派：子任務彼此獨立、可以同時進行——單一 Agent 只能一件事做完才做下一件，天生無法平行。",
     "或者：子任務推理量大，全部塞進主線對話會讓 context 迅速爆滿、推理跟著變混亂。",
     "解法：委派（delegation）——讓子 Agent 在自己乾淨的 context 裡把髒活做完，只把結論帶回主線；多個子任務一次派工，就能真正平行處理。"],
    DIAG_DELEGATE, src="CH.07",
    impl=["模型面向的入口是 delegate_task 工具，實作於 tools/delegate_tool.py（超過 5,000 行）。",
          "工具描述原文的兩個觸發條件：「reasoning-heavy subtasks...that would flood your context」與「independent parallel workstreams」。",
          "每個委派任務的即時逐字稿另外寫進 cache/delegation/live/<id>/task-<n>.log，方便旁觀進度，不進對話歷史的資料庫。"]),
  S("multiagent-2","隔離邊界",
    ["例外：工作目錄下的專案規則檔會被嵌入子 Agent 系統提示。",
     "回傳同樣受限：父層只收到最終結構化摘要，完整過程留在子 Agent 自己的 session。"],
    DIAG_KNOWNOTHING, links=[("identity-6","這份專案規則檔是什麼：Identity")], src="CH.07",
    impl=["隔離參數：skip_context_files=True、skip_memory=True、platform=\"subagent\"，並用 parent_session_id 追蹤家系。",
          "這份專案規則檔，就是後面 Identity 一節會細談的 AGENTS.md。"]),
  S("multiagent-3","實作本質",
    ["換一份系統提示、限縮工具清單，跑在同進程的另一條執行緒（thread pool）。",
     "不是另開行程，也不是特殊架構。"],
    DIAG_SAMECLASS, links=[("tools-1","委派沿用相同工具協定：Tools")], src="CH.07",
    impl=["呼叫鏈：child.run_conversation(user_message=goal, ...) 送進執行緒池（_timeout_executor.submit）。"]),
  S("multiagent-4","背景執行",
    ["頂層委派：強制背景執行，父層立即取得任務代號繼續執行。",
     "orchestrator（被授權可以再往下派工的子 Agent 角色）再往下委派：強制同步等待結果。",
     "深度預設扁平，多層委派需顯式設定 orchestrator 角色。"],
    DIAG_DEPTH, src="CH.07",
    impl=["判斷函式 _model_background_value()：depth=0 一律 background=True，depth&gt;0 一律 background=False；MAX_DEPTH 預設 1。"]),
  S("multiagent-5","Mixture of Agents",
    ["單一模型的判斷可能有偏差或遺漏——Mixture of Agents（MoA）讓多個「顧問」（Reference）模型各自先分析，再由一個 Aggregator 彙總、真正動手。",
     "不是額外的迴圈，而是包裝成一個虛擬的 model provider——選它就跟選任何一個模型一樣。"],
    DIAG_MOA, src="CH.14",
    impl=["實作於 agent/moa_loop.py；顧問角色的固定提示與工具排除邏輯集中在同一檔案。"]),
  S("multiagent-6","Reference／Aggregator",
    ["Reference：輕量、無工具權限、固定顧問角色提示，僅產出分析。",
     "Aggregator：接收全部分析作為參考資料，唯一具工具呼叫權限者。",
     "小結：委派解決 context 過載與平行處理，MoA 是多視角比對——兩種都是「讓不只一個模型參與」的答案。但不管用哪一種，最終都要接上一致的身份與情境規則——這是下一節 Identity 的主題。"],
    DIAG_ROLES, src="CH.14"),
],
"identity": [
  S("identity-5","SOUL.md",
    ["SOUL.md 只認這個 Hermes 實例本身（HERMES_HOME），完全不看你在哪個資料夾啟動。",
     "刻意設計：避免同一個 Hermes 因為專案目錄不同而表現出不同「性格」。",
     "怎麼被更新：agent 自己從不改——只有首次啟動填入預設範本，或使用者自己手動編輯。"],
    DIAG_SOUL, src="CH.15",
    impl=["load_soul_md() 只讀 (home_override 或 get_hermes_home()) / \"SOUL.md\"，程式碼裡沒有任何 cwd 回退路徑。",
          "使用者實際客製化過的 SOUL.md，系統再也不會去動它——首次啟動的預設範本只補「還是空白」的安裝。"]),
  S("identity-6","AGENTS.md",
    ["跟 SOUL.md 相反：AGENTS.md 從專案根目錄（git root）到你實際所在的資料夾（cwd）逐層合併，子目錄採漸進式發現，實際存取時才載入。",
     "越深層的規則排在越後面——等於用更具體的規則去補充、覆蓋前面的通則，同時避免塞爆 context、維持 prompt 快取不被打斷。",
     "怎麼被更新：agent 可以寫，但只有使用者明確下 /init 指令才會寫——不是自動背景流程，其餘時候唯讀。"],
    DIAG_AGENTSMD, links=[("context-2","原理依據：快取前綴比對")], src="CH.13",
    impl=["鏈式合併與漸進式子目錄發現是兩個獨立函式：前者一次載入整條鏈，後者只在工具實際碰到該子目錄時才觸發。",
          "相容格式：.hermes.md → AGENTS.md → CLAUDE.md → .cursorrules，第一個命中即用，其餘不再找。",
          "/init 觸發一輪特殊 agent 對話，用唯讀工具掃描專案後以 write_file 產生或合併更新 AGENTS.md。"]),
  S("identity-8","md 檔案總覽",
    ["四份 md 檔案，範圍、誰更新、怎麼被讀取都不一樣——別被「都是 md」騙了。",
     "小結：這一節談的是模型的身份與情境規則怎麼被決定；但知道「自己是誰」之後，模型還需要知道怎麼「用好」前面補上的每一種能力——這是最後一節 Guidance/Prompts 的主題。"],
    DIAG_MDTABLE, src="CH.13／CH.15"),
],
"guidance": [
  S("guidance-1","多套背景模板",
    ["五套提示詞模板裡，只有主系統提示是使用者間接看得到效果的；壓縮摘要、Subagent 提示、Curator 審查、Session 命名，全部是模型與使用者都感知不到的背景任務。",
     "這些背景任務共用同一條輔助模型解析鏈（任務專屬設定優先，找不到才逐層退回其他選項）——壓縮摘要用的就是這條鏈。"],
    DIAG_PROMPTS_MANY, links=[("context-4","輔助模型實際用在哪：Context 維護")], src="CH.17",
    impl=["共用機制為 agent/auxiliary_client.py；Curator 與壓縮摘要僅任務名稱不同（auxiliary.curator.model／auxiliary.compression.model）。"]),
  S("guidance-2","八層堆疊",
    ["①SOUL.md ②工具／模型guidance ③平台線索 ④專案情境檔 ⑤Skills索引 ⑥記憶 ⑦時間戳 ⑧/personality。",
     "①–⑦整體快取；第⑧層每次呼叫另外串接，不影響前七層的快取穩定性。"],
    DIAG_PROMPTSTACK, src="CH.15",
    impl=["/personality 對應的 ephemeral_system_prompt 明確被排除在快取字串之外，每次 API 呼叫時另外串接。"]),
  S("guidance-3","設計原則",
    ["高風險任務（如 Curator 審查）：規則逐條列舉，邊界案例明確約束。",
     "低風險任務（如 Session 命名）：保留較大的模型自主判斷空間。"],
    DIAG_RISKRULE, src="CH.17",
    impl=["Curator 審查提示的具體規則範例：「不准刪除任何 skill，最重動作是歸檔」「pinned=yes 的 skill 完全跳過，不准碰」。"]),
  S("guidance-5","總結",
    ["Tools 補行動力、Multi-Agent 補平行與 context 過載、Identity 補身份與情境設定、Skills 補特定流程、Memory 補跨 session、Guidance/Prompts 補「怎麼用好前五者」——Context 維護貫穿全部，不是第七個。",
     "這六個答案不是 hermes-agent 專屬的巧思，而是任何人動手做 harness 都會被逼著回答的問題——換一個場景、換一種取捨，你也能推出自己的答案。"],
    DIAG_RECAP, links=[("core-1","回到起點：什麼是 Harness")], src="CH.17"),
],
}

all_ids = set()
for c, sl in SLIDES.items():
    for s in sl:
        all_ids.add(s["id"])
missing = []
for c, sl in SLIDES.items():
    for s in sl:
        for target, label in s["links"]:
            if target not in all_ids:
                missing.append((s["id"], target))
if missing:
    raise SystemExit("BROKEN LINKS: " + str(missing))

# verify every arrow marker reference resolves within its own diagram
import re
bad_arrows = 0
for c, sl in SLIDES.items():
    for s in sl:
        d = s["diagram"]
        if not d: continue
        marker_ids = set(re.findall(r'<marker id="([^"]+)"', d))
        used = re.findall(r'marker-end="url\(#([^"]+)\)"', d)
        for u in used:
            if u not in marker_ids:
                bad_arrows += 1
                print("BROKEN ARROW in", s["id"], ":", u, "not in", marker_ids)
print("Broken arrows:", bad_arrows)
print("All links valid. Total slides:", sum(len(v) for v in SLIDES.values()))
print("Slides with diagrams:", sum(1 for sl in SLIDES.values() for s in sl if s["diagram"]))

json.dump({"clusters": CLUSTERS, "slides": SLIDES}, open('/tmp/slides.json','w',encoding='utf-8'), ensure_ascii=False)
print("saved /tmp/slides.json")
