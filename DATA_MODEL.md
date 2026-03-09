# MPNerveBot Data Model

Date: 2026-03-09

## Design Principles

- one Telegram chat can manage multiple marketplace accounts
- one account record maps to one marketplace connection
- onboarding state must survive restarts
- alert thresholds are per chat, not global
- event history should be persisted to avoid duplicate sends

## Tables

### `telegram_users`

Purpose:
- identify the Telegram actor and default chat

Fields:
- `id` integer primary key
- `telegram_user_id` integer unique not null
- `chat_id` integer not null
- `username` text null
- `first_name` text null
- `last_name` text null
- `created_at` text not null
- `updated_at` text not null

### `marketplace_accounts`

Purpose:
- store one marketplace connection per chat

Fields:
- `id` integer primary key
- `chat_id` integer not null
- `marketplace` text not null
- `display_name` text not null
- `connection_mode` text not null
- `status` text not null
- `credentials_json` text null
- `use_mock` integer not null default 1
- `last_validated_at` text null
- `last_sync_at` text null
- `last_error_text` text null
- `created_at` text not null
- `updated_at` text not null

Constraints:
- unique on `chat_id + marketplace`

Allowed values:
- `marketplace`: `wb`, `ozon`
- `connection_mode`: `mock`, `api`, `manual_pilot`
- `status`: `pending`, `connected`, `invalid`, `paused`

### `alert_settings`

Purpose:
- per-chat thresholds

Fields:
- `id` integer primary key
- `chat_id` integer unique not null
- `stock_days_threshold` integer not null default 5
- `sales_drop_percent_threshold` integer not null default 30
- `review_age_hours_threshold` integer not null default 24
- `digest_enabled` integer not null default 1
- `alerts_enabled` integer not null default 1
- `created_at` text not null
- `updated_at` text not null

### `onboarding_sessions`

Purpose:
- persist onboarding progress across restart or deployment

Fields:
- `id` integer primary key
- `chat_id` integer unique not null
- `state` text not null
- `selected_marketplace` text null
- `payload_json` text null
- `created_at` text not null
- `updated_at` text not null

Typical states:
- `idle`
- `choose_marketplace`
- `enter_ozon_credentials`
- `enter_wb_token`
- `confirm_demo_mode`
- `completed`

### `digest_history`

Purpose:
- avoid duplicate scheduled digests and keep minimal audit trail

Fields:
- `id` integer primary key
- `chat_id` integer not null
- `marketplace` text not null
- `digest_date` text not null
- `message_id` integer null
- `status` text not null
- `payload_json` text null
- `created_at` text not null

### `alert_events`

Purpose:
- deduplicate recurring alert spam

Fields:
- `id` integer primary key
- `chat_id` integer not null
- `marketplace` text not null
- `alert_type` text not null
- `dedupe_key` text not null
- `payload_json` text not null
- `sent_at` text not null

Constraints:
- unique on `chat_id + dedupe_key`

### `review_actions`

Purpose:
- track AI draft and seller decision

Fields:
- `id` integer primary key
- `chat_id` integer not null
- `marketplace` text not null
- `external_review_id` text not null
- `review_text` text not null
- `draft_reply_text` text null
- `action` text not null
- `created_at` text not null
- `updated_at` text not null

Allowed `action` values:
- `drafted`
- `sent`
- `edited`
- `skipped`

## Credential Storage Note

For MVP we should not keep seller credentials in code or in env vars.
Per-seller credentials must live in SQLite.

Because deployment is hosted on `Render`, next code step should encrypt `credentials_json` using an app secret from env.
If that is delayed for the first local-only milestone, it must be called temporary and removed before pilot onboarding.
