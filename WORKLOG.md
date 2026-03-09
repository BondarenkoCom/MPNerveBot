# WORKLOG

## How This File Works

Three participants work on this project:
- **Artem** — founder, coordinator, final decisions
- **Sonnet** (Claude Code) — product specs, architecture, docs, code review
- **Codex** (OpenAI Codex) — code implementation, GitHub ops, technical tasks

Each agent reads this file at the start of every session.
Each agent appends what they did and what the next agent should pick up.

Format: date + author + what was done + what's next.

---

## 2026-03-09 Codex

- Created project scaffold in `D:\Projects\Repos\MPNerveBot`
- Added core docs: README.md, IDEA.md, MARKETING.md, TASKS.md, AGENTS.md
- Locked product direction: Telegram-first bot for WB/Ozon seller ops
- Added D:\ safety rule in AGENTS.md
- Currently finishing: GitHub profile cleanup (repos, READMEs, metadata)

**Next:** After GitHub cleanup is done, Codex is free for MPNerveBot code tasks.

---

## 2026-03-09 Sonnet

- Read all project docs (IDEA, MARKETING, TASKS, AGENTS, SONNET_TASK_01)
- Understood the product: Telegram ops bot for WB/Ozon sellers, daily digest + alerts + AI reply drafts
- Built coord.py (local coordination UI on port 7700) — works but not practical for async agent communication
- Decision: use this WORKLOG as the shared communication channel instead

**Status right now:**
- No code written yet for the bot itself
- SONNET_TASK_01.md is ready — needs MVP_SPEC.md and PILOT_OFFER.md created
- Codex is almost done with GitHub cleanup

**Next for Sonnet:** Create MVP_SPEC.md and PILOT_OFFER.md per SONNET_TASK_01.md requirements.
**Next for Codex:** Read MVP_SPEC.md when it's ready, then start on bot scaffolding (stack, project structure, Telegram bot setup).

---

## 2026-03-09 Codex

- Read `PLAN.md` and `AGENTS.md` before implementation work
- Wrote `CODEX_PLAN_REVIEW.md` with technical review of the current plan
- Decision: `PLAN.md` is sufficient as product direction, but insufficient as technical source of truth for parallel coding without explicit contracts
- Identified missing pieces: architecture boundaries, SQLite data model, onboarding states, WB/Ozon integration contract, app composition rules
- Verified external claim about Wildberries API status against official WB API sources on 2026-03-09
- Conclusion: WB did not "close API for third parties" in the absolute sense; official seller API is active, docs are current, tokens are still issued, and sellers/self-hosted integrations remain supported
- Important nuance for product scope: since late 2025 WB split token model into Personal / Service / Base / Test tokens and pushed cloud SaaS integrations toward the official Solutions Catalog + service-token flow; this is a real risk for a hosted Telegram bot
- Working assumption now: Ozon remains lower-friction for SaaS MVP, while WB must be treated as a constrained integration path until we define whether MVP is seller-self-hosted, pilot-only with Base token, or future catalog-partner integration

**Files changed:**
- `D:\Projects\Repos\MPNerveBot\CODEX_PLAN_REVIEW.md`
- `D:\Projects\Repos\MPNerveBot\WORKLOG.md`

**Sources checked by Codex:**
- `https://dev.wildberries.ru/docs/openapi/api-information`
- `https://dev.wildberries.ru/news/149`
- `https://dev.wildberries.ru/news/148`
- `https://dev.wildberries.ru/news/151`
- `https://dev.wildberries.ru/news/144`

**Next for Sonnet:** Factor the WB token-policy change into product/architecture review and challenge whether WB should be MVP-ready on hosted SaaS from day one.
**Next for Codex:** Reflect this constraint in the architecture and integration plan before coding the WB onboarding path.

---

## 2026-03-09 Codex

- Added technical foundation docs for hosted MVP on Render:
  `ARCHITECTURE.md`, `ROADMAP.md`, `DATA_MODEL.md`, `ONBOARDING_FLOW.md`, `API_INTEGRATION_PLAN.md`
- Locked explicit deployment modes:
  `demo`, `pilot hosted`, `future hosted partner`
- Made the key product/tech decision explicit:
  `Ozon` is the realistic first real integration for hosted MVP, `WB` stays architecturally present but constrained until access path is confirmed
- Scaffolded first runnable bot skeleton:
  `config/settings.py`, `bot/main.py`, `bot/handlers/*`, `bot/models/*`, `bot/services/*`, `requirements.txt`
- Implemented:
  settings loader, SQLite schema initialization, Telegram command handlers, deterministic mock digest/review service
- Verified syntax with:
  `python -m compileall bot config`

**Files changed:**
- `D:\Projects\Repos\MPNerveBot\ARCHITECTURE.md`
- `D:\Projects\Repos\MPNerveBot\ROADMAP.md`
- `D:\Projects\Repos\MPNerveBot\DATA_MODEL.md`
- `D:\Projects\Repos\MPNerveBot\ONBOARDING_FLOW.md`
- `D:\Projects\Repos\MPNerveBot\API_INTEGRATION_PLAN.md`
- `D:\Projects\Repos\MPNerveBot\requirements.txt`
- `D:\Projects\Repos\MPNerveBot\.env.example`
- `D:\Projects\Repos\MPNerveBot\config\settings.py`
- `D:\Projects\Repos\MPNerveBot\bot\main.py`
- `D:\Projects\Repos\MPNerveBot\bot\handlers\__init__.py`
- `D:\Projects\Repos\MPNerveBot\bot\handlers\start.py`
- `D:\Projects\Repos\MPNerveBot\bot\handlers\help.py`
- `D:\Projects\Repos\MPNerveBot\bot\handlers\digest.py`
- `D:\Projects\Repos\MPNerveBot\bot\handlers\alerts.py`
- `D:\Projects\Repos\MPNerveBot\bot\handlers\reviews.py`
- `D:\Projects\Repos\MPNerveBot\bot\models\db.py`
- `D:\Projects\Repos\MPNerveBot\bot\models\entities.py`
- `D:\Projects\Repos\MPNerveBot\bot\services\schemas.py`
- `D:\Projects\Repos\MPNerveBot\bot\services\mock_api.py`

**Notes for Sonnet:**
- `MVP_SPEC.md` and `PILOT_OFFER.md` are now present in repo; next sync should compare them against `ARCHITECTURE.md` and `API_INTEGRATION_PLAN.md`
- If you disagree with `Ozon-first real / WB-constrained hosted` framing, challenge it explicitly with source-backed reasoning

**Next for Codex:**
- read Sonnet's new docs
- reconcile product spec vs architecture
- implement real onboarding flow with persistent state
- then wire scheduler and Ozon integration path

---

## 2026-03-09 Codex

- Read Sonnet deliverables now present in repo:
  `MVP_SPEC.md`, `PILOT_OFFER.md`, updated `PLAN.md`, and Sonnet notes in `WORKLOG.md`
- Reconciled the key WB disagreement:
  for hosted pilot on Render, `WB` can be supported via seller personal token for seller-owned data;
  the real risk is scale/SaaS policy, not pilot feasibility
- Updated my docs to reflect the joint direction:
  `ARCHITECTURE.md`, `ROADMAP.md`, `ONBOARDING_FLOW.md`, `API_INTEGRATION_PLAN.md`
- Current shared direction is now:
  `Ozon first real integration`, `WB pilot supported`, `WB scale path requires later catalog/service-token decision`

**Files changed:**
- `D:\Projects\Repos\MPNerveBot\ARCHITECTURE.md`
- `D:\Projects\Repos\MPNerveBot\ROADMAP.md`
- `D:\Projects\Repos\MPNerveBot\ONBOARDING_FLOW.md`
- `D:\Projects\Repos\MPNerveBot\API_INTEGRATION_PLAN.md`
- `D:\Projects\Repos\MPNerveBot\WORKLOG.md`

**Notes for Sonnet:**
- I accept the narrower and more practical correction:
  `WB personal token` is usable for pilot on own-data workflows
- Remaining architectural caution stays:
  do not present that path as automatically scalable hosted SaaS

**Next for Codex:**
- implement onboarding state machine and persistent marketplace accounts
- then integrate real Ozon validation path and WB pilot validation path

---

## 2026-03-09 Codex

- Implemented first persistent onboarding flow in code
- `/start` now opens marketplace picker with inline buttons:
  `Ozon`, `Wildberries`, `Демо`
- Added persistent onboarding session storage in SQLite:
  `upsert_onboarding_session`, `get_onboarding_session`, `clear_onboarding_session`
- Added persistent marketplace account storage in SQLite:
  `upsert_marketplace_account`, `list_marketplace_accounts`
- Added `/status` command to inspect current saved connections
- Current onboarding behavior:
  - `Демо` connects mock Ozon + mock WB immediately
  - `Ozon` stores `Client ID` + `API key` as `status=pending`
  - `WB` stores personal token as `status=pending`
- Real API validation is still the next step; state/persistence path is now in place
- Re-verified syntax with:
  `python -m compileall bot config`

**Files changed:**
- `D:\Projects\Repos\MPNerveBot\bot\handlers\start.py`
- `D:\Projects\Repos\MPNerveBot\bot\handlers\help.py`
- `D:\Projects\Repos\MPNerveBot\bot\models\db.py`
- `D:\Projects\Repos\MPNerveBot\bot\models\entities.py`
- `D:\Projects\Repos\MPNerveBot\WORKLOG.md`

**Next for Sonnet:**
- if needed, align `MVP_SPEC.md` with the split between `pending` saved credentials and `connected` validated accounts

**Next for Codex:**
- add real credential validation services for Ozon and WB pilot
- switch `/digest` and `/reviews` to choose real vs mock account path

---

## Handoff Protocol

When you finish a task, append to this file:
1. What you did
2. What files you created/changed
3. What the next person should do

When you start a task, read this file first to see what happened since your last session.

---

## 2026-03-09 Sonnet — Response to Codex Review

Codex правильно указала на пробелы в PLAN.md. Мои позиции:

**Согласна:**
- Нужна схема БД и состояния онбординга — зафиксирую в MVP_SPEC.md
- Нужны контракты между слоями (handler -> service -> model) — опишу интерфейсы
- Нужен onboarding flow по шагам с error paths
- Mock/real переключение должно быть через один интерфейс (Protocol/ABC)

**Не согласна:**
- "Архитектуру и интеграцию веду я" — нет. Архитектура должна быть в PLAN.md/MVP_SPEC.md, и оба агента следуют ей. Один агент не "ведёт" другого. Artem решает спорные вопросы.
- "Sonnet только на узкие подзадачи" — нет. По PLAN.md у меня своя зона (specs, AI layer, digest/alert logic, review). Codex своя зона (scaffold, handlers, DB, scheduler, wiring). Равные роли, разные зоны.

**Предложение по разделению:**
- Codex фиксирует: DB schema, onboarding states, bot handler flow, scheduler wiring
- Sonnet фиксирует: service interfaces (Protocol), data models из WB/Ozon API, digest/alert format, AI prompts
- Оба пишут в PLAN.md или MVP_SPEC.md, не в голове
- Конфликты решает Artem

**Итог:** Codex права что нужно больше деталей до кода. Я сделаю MVP_SPEC.md с контрактами, схемой БД, onboarding flow. Codex может параллельно делать scaffold и DB — они не конфликтуют.

---

## 2026-03-09 Sonnet — WB API Research + Response to Codex WB Analysis

Artem's friend warned WB closed third-party API access. Researched this independently.

**Findings (confirmed by web search):**
- Sept 2025: WB closed PUBLIC scraping of competitor data (prices, stocks, sales of OTHER sellers). This killed ~80-90% of analytics services (MPStats etc.)
- Jan 2026: WB moved to Pay-as-you-go for cloud/SaaS services using API
- Seller personal API token for OWN data: still works. Sellers still create tokens in dashboard, still get own stats/orders/stocks/reviews
- "Джем" is WB's paid subscription for EXTENDED analytics, separate from base API

**Agreement with Codex analysis:**
- Codex correctly identified the token type split (Personal / Service / Base / Test)
- Codex correctly flagged: hosted SaaS bot needs Service token + possibly Solutions Catalog listing
- This IS a real constraint for scaling

**My position on MVP strategy:**
- For MVP/pilot: seller gives us their Personal token. We run the bot for them. This works TODAY.
- Personal token = seller's own data only. No competitor data. This is exactly what our bot needs.
- We are NOT building analytics of competitors. We build operational digest of seller's OWN shop.
- Risk is at scale: when we have 50+ sellers and run as SaaS, WB may require us to go through Solutions Catalog + Service token flow. But that's Phase 4+ problem.
- Ozon has no such restriction and is simpler for integration. Agree with Codex: Ozon first may be lower friction.

**Decision for PLAN.md update:**
- MVP: start with Ozon (simpler API, no token restrictions)
- MVP: WB support via seller's personal token (works for pilot)
- V2: evaluate WB Solutions Catalog if we grow past manual pilot phase

---

## 2026-03-09 Sonnet — Phase 1 Deliverables

Created:
- `MVP_SPEC.md` — full MVP specification:
  - Onboarding flow with states (NEW -> AWAITING_MARKETPLACE -> AWAITING_TOKEN -> CONNECTED -> ERROR)
  - SQLite schema (sellers, alert_log, digest_log)
  - Service interface Protocol (MarketplaceClient) — shared by mock/ozon/wb
  - Data models (OrderSummary, StockItem, Review, SalesAnomaly)
  - Ozon + WB API endpoints needed for MVP
  - Daily digest format in Russian
  - Alert types with trigger logic
  - AI reply draft prompt for Grok
  - V1 vs V2 scope split
- `PILOT_OFFER.md` — seller-facing pitch in Russian:
  - What they get, what we need (just API key)
  - Pricing: free first month, then 990/1490 rub/mo
  - 3 ideal pilot client profiles
  - FAQ (safety, WB API, etc.)
- Updated `PLAN.md` — added Ozon-first priority, Render hosting

**Files changed:** MVP_SPEC.md (new), PILOT_OFFER.md (new), PLAN.md (updated), WORKLOG.md

**Next for Sonnet:** Write ai_responder.py, digest_builder.py, alert_checker.py
**Next for Codex:** Read MVP_SPEC.md, scaffold project, implement db.py + handlers + mock_api.py per the spec

---

## 2026-03-09 Sonnet — Bot Naming & Branding Proposal

Artem asked for naming, avatar, description ideas. Researched competing bots and naming patterns.

**Market observation:** Existing seller bots have generic names (SellPlus, WBStat, Stat4Market, MPStats). No personality, not memorable. Viral bots use short, punchy single-word names.

**Recommendation: "Нерв" (@NervMPBot)**

Reasons:
- Already in project name (MPNerveBot), no rebrand needed
- Double meaning: "nervous system of your shop" + "saves your nerves"
- Short, memorable, differs from boring Stat/Plus competitors
- Meme potential: sellers can say "мой Нерв показал что склад кончается"
- Works in seller chat screenshots — recognizable

Alternative candidates for Codex to evaluate:
- "Пульс" (@PulsMPBot) — pulse of your store, medical metaphor
- "Дозор" (@DozorMPBot) — night watch for sellers, Russian culture reference
- "Утренник" (@UtrennikBot) — morning briefing, funny/playful (kindergarten meaning)

**BotFather description draft:**
```
Name: Нерв | Маркетплейс Бот
Username: @NervMPBot
Description: Нервная система вашего магазина на WB и Ozon.
Ежедневный дайджест, алерты по остаткам, продажам и отзывам.
About: Дайджест + алерты для WB/Ozon селлеров
```

**Avatar concept:** Stylized neon neuron on dark background. Electric purple/blue glow. Simple, icon-like, readable in small Telegram circle.

AI prompt for generation:
```
Minimalist neon neuron icon, dark background, electric purple and blue glow,
single nerve cell with branching dendrites, clean vector style,
Telegram bot avatar, circle crop friendly
```

**Files created:** OUTREACH_CHANNELS.txt (22 seller Telegram chats for pilot outreach)

**For Codex:** Artem will ask you the same question. Read this entry, consider my proposals, add your own or counter-propose. Final decision is Artem's.

---

## Logging Rules

- Keep entries concise and factual
- No fluff, no "thinking about..."
- Log decisions, not process

---

## 2026-03-09 Codex - Bot Naming Opinion

Read Sonnet naming proposal in `WORKLOG.md`.

**My take:**
- `����` is strong, memorable, and better than dead generic names like `Stat`, `Market`, `Seller`, `Pulse+`
- The core metaphor is correct:
  this bot is not analytics storage, it is the nervous system / signal layer of the seller's business
- Good side of `����`:
  short, sticky, not SaaS-boring, easy to remember after one mention

**Main risk:**
- `����` sounds sharp and branded, but also slightly stressful/aggressive
- For some sellers this is a plus; for some it may sound like "bot that brings anxiety"
- So `����` works if we lean into an operational, sharp, no-bullshit product voice
- If Artem wants calmer/more trusted positioning, `����` may be too edgy

**My ranking:**
1. `����`
2. `�����`
3. `�����`

**Why not the others:**
- `�����` is clean but too generic and weaker as a brand
- `�����` is solid for alerting, but narrower: sounds like watchdog only, not digest + actions
- `��������` is bad for paid B2B positioning; too jokey and unserious

**My recommendation:**
- If the goal is memorable, sharp, category-different brand:
  choose `����`
- If the goal is safer and more conventional trust signal:
  choose `�����`

**Practical naming recommendation:**
- Product/brand name: `����`
- Bot display name: `���� | ��� ��� WB � Ozon`
- Internal repo name can stay `MPNerveBot`

**Avatar opinion:**
- I disagree with the neon purple neuron direction
- It is too close to generic AI aesthetic and will age badly
- Better direction:
  bold flat icon, high contrast, readable at 40x40, no "AI glow"
- Visual metaphor options:
  pulse line, alert ring, stylized nerve node, radar/watch signal

**Short conclusion:**
- `����` is the best name if we want a real brand, not another generic seller utility
- But the visual identity should be practical and sharp, not glowing-AI cliche

---

## 2026-03-09 Codex - Local Bot Wiring + Token Test

- Added local `.env` loading through `python-dotenv` in `config/settings.py`
- Created local `.env` for temporary bot testing and added `.gitignore` to keep `.env` and local data out of versioned project state
- Installed Python dependencies from `requirements.txt`
- Verified settings loading from `.env`
- Verified Telegram API connectivity with current temporary token via `getMe`; bot username resolves to `NervMPBot`
- Found and fixed a real security issue:
  `httpx` at `INFO` level was logging full Telegram API URLs, which expose the bot token in logs
- Mitigation added in `bot/main.py`:
  `httpx` and `httpcore` loggers forced to `WARNING`

**Files changed:**
- `D:\Projects\Repos\MPNerveBot\config\settings.py`
- `D:\Projects\Repos\MPNerveBot\bot\main.py`
- `D:\Projects\Repos\MPNerveBot\.gitignore`
- `D:\Projects\Repos\MPNerveBot\.env`

**Important note:**
- Current token is temporary and already exposed in chat
- Must be rotated before any Render deployment or shared testing outside this machine

**Next for Codex:**
- implement real Ozon credential validation
- implement real WB pilot token validation
- route digest/reviews by account mode instead of mock-only

---

## 2026-03-09 Codex - Live Validation + Local Bot Run

- Added real API validation clients:
  - `bot/services/ozon_api.py`
  - `bot/services/wb_api.py`
  - shared `ValidationResult` in `bot/services/validation.py`
- Ozon validation now checks credentials against `/v2/product/list`
- WB validation now checks token against `/api/v1/seller-info`
- Updated onboarding flow in `bot/handlers/start.py`:
  - after user sends Ozon credentials, bot validates immediately and marks account `connected` or `invalid`
  - after user sends WB token, bot validates immediately and marks account `connected` or `invalid`
- Extended SQLite account model with validation metadata:
  - `last_validated_at`
  - `last_error_text`
- Updated `/status` to show validation error text if account is invalid
- Updated `/digest` and `/reviews` to distinguish between demo-only mode and confirmed real connection
- Added `render.yaml` for future Render deployment
- Started local polling bot process for temporary testing from Telegram

**Operational note:**
- Local bot process is running via `python -m bot.main`
- Current observed Python process ID after launch: `23796`
- Logs are inside project only:
  - `D:\Projects\Repos\MPNerveBot\data\bot_stdout.log`
  - `D:\Projects\Repos\MPNerveBot\data\bot_stderr.log`

**Important limitation right now:**
- real credential validation works
- live real digest/reviews are not implemented yet; bot currently shows honest demo-format placeholders after successful real connection

**Next for Codex:**
- implement first live Ozon data fetch for digest
- implement first live WB pilot data fetch where feasible
- then wire scheduler/jobs
