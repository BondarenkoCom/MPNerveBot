# MPNerveBot — Master Plan

This is the single source of truth for what we build and who does what.
Both agents (Sonnet + Codex) read this file before starting any work.

---

## What We're Building

Telegram bot for WB/Ozon sellers. Not a dashboard — an operations layer.
The seller connects their marketplace API token, gets a daily digest and alerts in Telegram.

## Marketplace Priority

Ozon first — simpler API, no token restrictions for third-party integrations.
WB second — works via seller's personal token for pilot, but has SaaS restrictions at scale (Solutions Catalog + Service token required). See WORKLOG for full analysis.

## Hosting

Render (existing server). Bot runs as a long-running service.

## Stack

- Python 3.11+
- python-telegram-bot (async)
- httpx for marketplace API calls
- SQLite for local state (seller tokens, alert config, message history)
- Grok API (xAI) for AI features (cheap: $0.20/1M tokens)
- Mock layer for WB/Ozon APIs until we have a real seller token
- Hosted on Render

## Project Structure

```
MPNerveBot/
  bot/
    __init__.py
    main.py              # entry point, bot startup
    handlers/
      __init__.py
      start.py           # /start, onboarding flow
      digest.py          # /digest command
      alerts.py          # alert settings
      feedback.py        # review reply flow
    services/
      __init__.py
      wb_api.py          # Wildberries API client
      ozon_api.py        # Ozon API client
      mock_api.py        # mock data layer (used until real tokens)
      digest_builder.py  # formats daily digest message
      alert_checker.py   # checks stock levels, sales drops, unanswered reviews
      ai_responder.py    # generates draft replies via Grok
    models/
      __init__.py
      db.py              # SQLite schema + helpers
      seller.py          # seller model (token, marketplace, chat_id)
    scheduler/
      __init__.py
      daily.py           # cron-like daily digest sender
      watcher.py         # periodic alert checks
  config/
    settings.py          # env vars, defaults
  ref/                   # reference code from AIJobSearcher (read-only)
    ref_llm_client.py
    ref_telegram_notify.py
  tests/
    test_digest.py
    test_alerts.py
    test_mock_api.py
  .env.example
  requirements.txt
  PLAN.md               # this file
```

---

## MVP Features (V1)

### 1. Onboarding
- /start — choose marketplace (WB / Ozon / both)
- paste API token
- bot confirms connection, saves to SQLite

### 2. Daily Digest (sent at 09:00 Moscow time)
```
Digest for March 10:

Orders: 47 (+12% vs yesterday)
Revenue: 128,400 rub
Returns: 3

Stock alerts:
  - SKU "Blue T-Shirt XL" — 4 days left
  - SKU "Phone Case Black" — 2 days left

Reviews: 3 unanswered
  oldest: 2 days ago

Top anomaly: "Blue T-Shirt XL" sales dropped 40% vs 7-day avg
```

### 3. Alerts (checked every 2 hours)
- Stock < N days left (default: 5 days)
- Sales drop > 30% vs 7-day average
- Unanswered review older than 24h

### 4. AI Reply Drafts
- Bot shows new review text
- Generates draft reply via Grok
- Buttons: [Send as is] [Edit] [Skip]

### 5. Commands
- /start — onboarding
- /digest — get digest now
- /alerts — configure alert thresholds
- /reviews — list unanswered reviews
- /help — command list

---

## Mock Layer

Until we have a real seller token, all marketplace data comes from `mock_api.py`.
It returns realistic fake data: 50-80 orders/day, 5-15 SKUs, some with low stock, some reviews.
The mock layer implements the same interface as `wb_api.py` / `ozon_api.py`.

---

## Who Does What

### Sonnet (Claude Code)
1. Create MVP_SPEC.md with detailed API response formats
2. Create PILOT_OFFER.md (seller-facing pitch)
3. Design mock data shapes (what mock_api returns)
4. Write ai_responder.py (adapt from ref/ref_llm_client.py)
5. Write digest_builder.py (formatting logic)
6. Write alert_checker.py (threshold logic)
7. Review Codex's code

### Codex (OpenAI)
1. Scaffold project structure (folders, __init__.py, requirements.txt)
2. Write bot/main.py + handlers (Telegram bot setup)
3. Write models/db.py (SQLite schema)
4. Write services/wb_api.py + ozon_api.py (API client stubs)
5. Write services/mock_api.py (fake data generator)
6. Write scheduler/ (daily digest cron, alert watcher)
7. Wire everything together

### Artem
1. Find first pilot seller (Telegram communities)
2. Create Telegram bot via @BotFather
3. Test the bot manually
4. Write outreach messages for sellers

---

## Execution Order

```
Phase 1 — Skeleton (both agents, parallel)
  Sonnet: MVP_SPEC.md, PILOT_OFFER.md, digest format, alert logic
  Codex:  project scaffold, bot handlers, SQLite, mock layer

Phase 2 — Wiring (Codex leads, Sonnet reviews)
  Codex:  connect handlers to services, scheduler
  Sonnet: ai_responder.py, review Codex code

Phase 3 — Polish (both)
  Russian language in all bot messages
  Error handling, token validation
  Test with mock data end-to-end

Phase 4 — Real Data (needs pilot seller)
  Artem provides WB/Ozon API token
  Switch from mock to real API
  Fix edge cases on real data
```

---

## Rules

- All bot messages in Russian
- No English in user-facing text
- Keep code simple, no over-engineering
- Mock layer is first-class, not an afterthought
- Every service has a clear interface (so mock and real are swappable)
- Log decisions in WORKLOG.md
