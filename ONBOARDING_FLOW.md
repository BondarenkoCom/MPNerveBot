# MPNerveBot Onboarding Flow

Date: 2026-03-09

## Goal

Connect a seller to useful bot output with the smallest possible friction.

## Primary Paths

### Path A: Demo Mode

Use when:
- local development
- product demo
- no real marketplace credentials yet

Flow:
1. User sends `/start`
2. Bot explains value in one short message
3. Bot offers choices: `Ozon`, `Wildberries`, `Демо`
4. User picks `Демо`
5. Bot enables mock mode
6. Bot sends next-step commands: `/digest`, `/reviews`, `/alerts`

### Path B: Ozon Real Connection

Use when:
- hosted MVP on Render
- real seller wants pilot

Flow:
1. User sends `/start`
2. Bot asks marketplace
3. User picks `Ozon`
4. Bot asks for `Client ID` and `API key`
5. Bot stores credentials and runs validation
6. If valid, bot creates `marketplace_accounts` record with `status=connected`
7. Bot confirms connection and enables digest/alerts

Error paths:
- invalid credential format
- API auth rejected
- temporary API outage

### Path C: WB Hosted Pilot

Use when:
- seller wants WB
- deployment is hosted on Render

Flow:
1. User sends `/start`
2. Bot picks `Wildberries`
3. Bot asks for seller personal token
4. Bot validates token against seller-owned data path
5. If valid, bot creates `marketplace_accounts` record with `status=connected`
6. Bot marks the account as `pilot` if needed for internal tracking
7. Bot confirms that WB is connected for pilot use on seller's own data

Critical rule:
- never pretend `WB` is a guaranteed scalable hosted SaaS path if we are still using seller personal tokens in pilot mode

## Message Rules

- short messages
- no API jargon unless needed
- no English
- every onboarding step must make the next action obvious

## State Machine

- `idle`
- `choose_marketplace`
- `confirm_demo_mode`
- `enter_ozon_credentials`
- `enter_wb_token`
- `validate_credentials`
- `connected`
- `blocked_policy`

## Command Behavior After Onboarding

- `/digest` returns latest digest now
- `/alerts` shows thresholds and alert state
- `/reviews` lists unanswered reviews
- `/help` shows supported actions

## Honest Scope For Current Hosted MVP

Current realistic order:
- `Demo` first
- `Ozon` real next
- `WB` pilot via seller personal token
- `WB` scaled SaaS path only after policy-compatible route is confirmed
