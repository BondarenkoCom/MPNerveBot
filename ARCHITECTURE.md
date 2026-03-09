# MPNerveBot Architecture

Date: 2026-03-09
Status: working foundation for MVP

## Product Shape

`MPNerveBot` is a hosted Telegram bot for marketplace sellers.
Runtime target: `Render`.
Primary interface: Telegram.
Primary deployment mode for MVP: one bot service, one persistent SQLite database on Render disk.

## Non-Goals

- no dashboard clone
- no generic SaaS platform
- no multi-tenant admin panel in V1
- no complex analytics warehouse

## Core Constraints

- all user-facing bot text is Russian
- project must stay Telegram-first
- `Render` means the app is hosted, not self-hosted
- official `Wildberries` API exists, but hosted third-party SaaS access has policy constraints
- because of that, MVP must treat `Ozon` as lower-friction real integration and `WB` as a pilot-capable but scale-constrained integration

## MVP Deployment Modes

We need explicit runtime modes, otherwise onboarding and integration logic will drift.

### Mode A: Demo

- both marketplaces use mock clients
- used for local development and first UX demo

### Mode B: Pilot Hosted

- `Ozon`: real API connection allowed
- `WB`: seller personal token allowed for pilot on seller's own data
- `WB` scaling risk remains and must stay explicit

### Mode C: Future Hosted Partner

- `Ozon`: real API
- `WB`: real API only after token/auth model is aligned with WB partner/catalog requirements

## Layering

### 1. `config/`

Loads environment variables and runtime settings.

Responsibilities:
- bot token
- base URL for webhook
- database path
- runtime mode
- scheduler settings

### 2. `bot/handlers/`

Telegram transport layer.

Responsibilities:
- parse commands and callbacks
- validate Telegram input shape
- call services
- send formatted replies

Must not:
- call marketplace HTTP directly
- contain SQL
- decide integration mode on their own

### 3. `bot/services/`

Application logic and external integrations.

Responsibilities:
- mock marketplace data
- marketplace client contracts
- digest building inputs
- review listing
- alert calculation inputs

### 4. `bot/models/`

Persistence and domain entities.

Responsibilities:
- SQLite schema
- account records
- alert settings
- onboarding session state

### 5. `bot/scheduler/`

Background jobs inside the bot process.

Responsibilities:
- daily digest at 09:00 Moscow time
- alert checks every 2 hours

For MVP this can run inside the Telegram process.
If Render scaling or uptime patterns become a problem, move scheduling to a dedicated worker.

## Composition Rules

There must be one composition root in `bot/main.py`.

It creates:
- settings
- database
- mock client
- future real clients
- Telegram application

It injects shared dependencies through `application.bot_data`.

Handlers read dependencies only from the application container.
They do not instantiate clients themselves.

## Marketplace Contract

All marketplace clients must expose the same high-level methods:

- `validate_credentials(...)`
- `get_daily_digest(...)`
- `get_unanswered_reviews(...)`
- `get_alert_snapshot(...)`

This is critical.
If mock and real clients return different shapes, parallel work will break.

## Data Flow

1. Seller opens bot and runs `/start`
2. Bot stores Telegram user and onboarding state
3. Seller connects marketplace credentials or uses demo mode
4. Bot stores marketplace account record
5. Scheduler or command requests a marketplace snapshot
6. Client returns normalized data shape
7. Handler/service formats Telegram message
8. Bot stores digest/alert event metadata

## Render Hosting Decision

For MVP on `Render`, use webhook mode when `APP_BASE_URL` is present.
Fallback to polling for local development.

Reason:
- webhook matches hosted deployment better
- polling stays useful for local dev and quick testing

## Immediate Architecture Decision

We should not market `WB` as a frictionless hosted SaaS path at scale from day one.

The honest MVP path is:
- demo mode for both marketplaces
- real `Ozon` integration first
- `WB` pilot integration via seller personal token for own-data use cases
- later transition to service-token/catalog path if scale requires it
