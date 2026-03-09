# MPNerveBot API Integration Plan

Date: 2026-03-09
Status: MVP planning document

## Source Policy

Use official docs first.
Do not design the integration from forum guesses.

Official references checked on 2026-03-09:
- [Wildberries API docs](https://dev.wildberries.ru/docs/openapi/api-information)
- [WB token connection guide, 2025-10-20](https://dev.wildberries.ru/news/149)
- [WB new token system, 2025-10-20](https://dev.wildberries.ru/news/148)
- [WB partner auth migration, 2025-09-25](https://dev.wildberries.ru/news/144)
- [WB cloud-service billing notice, 2025-10-23](https://dev.wildberries.ru/news/151)
- [Ozon Seller API intro](https://docs.ozon.ru/global/zh-hans/api/intro/)

## Integration Strategy

### Ozon

Target status for hosted MVP:
- real integration

Credential model:
- `Client ID`
- `API key`

Why Ozon first:
- official seller API is standard for external systems
- hosted SaaS path appears less constrained than current WB hosted policy

### Wildberries

Target status for hosted MVP:
- pilot-capable, scale-constrained

Credential model:
- seller personal token for pilot
- service-token/service-secret path for future scaled hosted integration

Risk:
- official docs are active, but hosted third-party cloud integrations are tied to stricter token/service policy

Decision:
- keep `WB` in architecture
- allow `WB` pilot onboarding via seller personal token for seller-owned data
- do not promise seamless hosted production onboarding at scale until the service-token/catalog path is confirmed

## Normalized Marketplace Contract

Every marketplace client must return the same normalized shapes.

### `validate_credentials`

Input:
- marketplace-specific credentials

Output:
- `is_valid`
- `account_name`
- `warnings`
- `error_text`

### `get_daily_digest`

Input:
- date
- chat account context

Output:
- `orders_count`
- `orders_delta_percent`
- `revenue_amount`
- `returns_count`
- `stock_risks[]`
- `unanswered_reviews_count`
- `oldest_review_age_hours`
- `top_anomaly`

### `get_unanswered_reviews`

Output item:
- `review_id`
- `product_name`
- `rating`
- `text`
- `created_at`
- `age_hours`

### `get_alert_snapshot`

Output:
- `stock_alerts[]`
- `sales_drop_alerts[]`
- `review_alerts[]`

## MVP Data Needed From APIs

### Ozon Needed Data

- sales/orders summary for the day
- revenue summary for the day
- return count
- stock/residual data by SKU
- unanswered review list or supportable equivalent
- product names for human-readable messages

### WB Needed Data

- same normalized business outputs as above
- for pilot this can come from seller personal token
- for scale this depends on service-token/catalog path

## Runtime Capability Flags

We need explicit runtime flags.

Suggested settings:
- `APP_MODE=demo|pilot`
- `OZON_REAL_ENABLED=true|false`
- `WB_REAL_ENABLED=true|false`

The bot should branch on these flags instead of hardcoded assumptions.

## Implementation Order

1. build mock client first
2. build Ozon validation client
3. build Ozon digest/review fetchers
4. build WB pilot validation path with seller personal token
5. wire scheduler against normalized contract
6. revisit WB service-token/catalog path before scale rollout

## Product Honesty Rule

If a marketplace path is constrained, the bot must say so.
Fake onboarding success is worse than a delayed integration.
