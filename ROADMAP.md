# MPNerveBot Roadmap

Date: 2026-03-09

## Phase 0: Technical Foundation

- lock architecture boundaries
- lock data model
- lock onboarding states
- lock normalized marketplace contract
- adjust assumptions for `Render` hosting and `WB` constraints

Deliverables:
- `ARCHITECTURE.md`
- `DATA_MODEL.md`
- `ONBOARDING_FLOW.md`
- `API_INTEGRATION_PLAN.md`
- initial project skeleton

## Phase 1: Bot Skeleton

- create Python package structure
- add settings loader
- add SQLite initialization
- boot Telegram app
- add `/start`, `/help`, `/digest`, `/alerts`, `/reviews`
- wire mock marketplace service

Success condition:
- bot runs locally
- bot responds in Russian
- `/digest` and `/reviews` work with mock data

## Phase 2: Onboarding and Persistence

- store Telegram user records
- store marketplace account records
- store onboarding sessions
- store alert thresholds
- complete onboarding happy path for demo mode and Ozon

Success condition:
- user can connect an account or enter demo mode
- data survives restart via SQLite

## Phase 3: Scheduled Jobs

- daily digest scheduler at 09:00 Moscow time
- alert watcher every 2 hours
- persist alert event history
- prevent duplicate sends after restart

Success condition:
- scheduled messages are delivered from Render

## Phase 4: Ozon Real Integration

- validate `Client ID` and `API key`
- pull metrics needed for digest
- pull stock/risk inputs
- pull unanswered review inputs
- handle API errors and quota issues

Success condition:
- one pilot seller works on real Ozon data

## Phase 5: WB Strategy Split

- keep WB demo path active
- support WB pilot via seller personal token
- verify long-term hosted access path
- decide between:
  - continued pilot token flow
  - self-hosted mode
  - partner/catalog integration later

Success condition:
- no fake promise in onboarding
- real technical path chosen before WB production rollout at scale

## Phase 6: AI Reply Flow

- add review reply draft generation
- add approve/edit/skip flow
- store review action history

Success condition:
- seller gets useful draft replies inside Telegram
