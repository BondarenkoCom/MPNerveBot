# Data Model

## Design Principles

- one Telegram chat can manage multiple marketplace connections
- onboarding state survives restarts
- alert settings are per chat
- event history prevents duplicate sends

## Main Tables

### `telegram_users`

Stores the Telegram actor and default chat.

### `marketplace_accounts`

Stores one account connection per chat and provider.

Typical provider values:

- `marketplace_a`
- `marketplace_b`

### `alert_settings`

Stores digest and alert thresholds per chat.

### `onboarding_sessions`

Stores in-progress onboarding state.

### `digest_history`

Stores sent digests.

### `alert_events`

Stores alert dedupe history.

### `review_actions`

Stores AI draft and review workflow actions.
