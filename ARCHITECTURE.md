# Architecture

## Overview

MPNerveBot is a hosted Telegram bot that acts as an operations layer for marketplace merchants.
The public repository is intentionally generic and avoids naming specific marketplace vendors.

## Layers

### `config/`

Loads environment variables and runtime settings.

### `bot/handlers/`

Telegram transport layer.
Parses commands, callbacks, and user input.

### `bot/services/`

Business logic and provider integration stubs.
In the public repo these are generic provider adapters.

### `bot/models/`

Persistence layer and domain entities.

### `bot/scheduler/`

Background jobs for digests and alerts.

## Runtime Modes

- `demo`
- `pilot`

## Composition

`bot/main.py` is the composition root.
It creates settings, database access, service instances, and the Telegram application.

## Provider Contract

All provider adapters should expose the same high-level methods:

- `validate_credentials(...)`
- `get_daily_digest(...)`
- `get_unanswered_reviews(...)`
- `get_alert_snapshot(...)`

## Public Showcase Constraint

Real provider names, proprietary workflows, and private integration details should not live in the public version of this repository.
