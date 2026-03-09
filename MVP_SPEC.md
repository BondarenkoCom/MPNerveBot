# MVP Specification

## User Roles

| Role | Description |
|------|-------------|
| Owner | Seller who connects their marketplace account. Full access. |
| Manager | Added by owner to shared Telegram group. Read-only digest + alerts. |

V1: Owner only. Manager support = V2.

---

## Onboarding Flow

```
User sends /start
  -> Bot: "Привет! Я помогу следить за вашим магазином на маркетплейсах.
           Выберите площадку:"
           [Ozon] [Wildberries] [Обе]

User taps [Ozon]
  -> Bot: "Отправьте ваш Ozon Client-ID и API-ключ через пробел.
           Найти их можно в Настройки > Seller API."

User sends: "123456 abcdef-key-here"
  -> Bot validates token by calling Ozon /v1/product/list (limit=1)
  -> Success: "Подключено! Нашла {N} товаров. Дайджест будет приходить каждый день в 09:00 МСК.
               /digest — получить дайджест сейчас
               /help — все команды"
  -> Fail: "Не удалось подключиться. Проверьте Client-ID и API-ключ и отправьте ещё раз."

User sends /start again (already connected)
  -> Bot: "Вы уже подключены ({marketplace}).
           /disconnect — отключить
           /help — все команды"
```

### Onboarding States (per user)

| State | Meaning |
|-------|---------|
| NEW | Just sent /start, no marketplace chosen |
| AWAITING_MARKETPLACE | Showed marketplace picker |
| AWAITING_TOKEN | Marketplace chosen, waiting for token |
| CONNECTED | Token validated, active |
| ERROR | Token was valid but stopped working |

---

## SQLite Schema

```sql
CREATE TABLE sellers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_chat_id INTEGER UNIQUE NOT NULL,
    telegram_username TEXT,
    marketplace TEXT NOT NULL,          -- 'ozon' | 'wb' | 'both'
    ozon_client_id TEXT,
    ozon_api_key TEXT,
    wb_token TEXT,
    onboarding_state TEXT NOT NULL DEFAULT 'NEW',
    digest_hour INTEGER NOT NULL DEFAULT 9,  -- Moscow time
    alert_stock_days INTEGER NOT NULL DEFAULT 5,
    alert_sales_drop_pct INTEGER NOT NULL DEFAULT 30,
    alert_review_hours INTEGER NOT NULL DEFAULT 24,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE alert_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    seller_id INTEGER NOT NULL REFERENCES sellers(id),
    alert_type TEXT NOT NULL,           -- 'low_stock' | 'sales_drop' | 'unanswered_review'
    sku_or_id TEXT,
    message TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE digest_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    seller_id INTEGER NOT NULL REFERENCES sellers(id),
    sent_at TEXT NOT NULL DEFAULT (datetime('now')),
    content TEXT NOT NULL
);
```

---

## Telegram Commands

| Command | Description (shown in /help) |
|---------|------------------------------|
| /start | Начать работу / подключить магазин |
| /digest | Получить дайджест прямо сейчас |
| /reviews | Показать неотвеченные отзывы |
| /alerts | Настроить пороги алертов |
| /status | Статус подключения |
| /disconnect | Отключить магазин |
| /help | Список команд |

---

## Daily Digest Format (Russian)

```
Дайджест за 10 марта

Заказы: 47 (+12% к вчера)
Выручка: 128 400 руб
Возвраты: 3

Остатки под угрозой:
  - "Футболка синяя XL" — осталось на 4 дня
  - "Чехол чёрный" — осталось на 2 дня

Отзывы без ответа: 3
  самый старый: 2 дня назад

Аномалия: "Футболка синяя XL" — продажи упали на 40% к среднему за 7 дней
```

If no issues: shorter version without alert sections.

---

## Alert Types

### 1. Low Stock
- Trigger: estimated days of stock < seller.alert_stock_days (default 5)
- Calculation: current_stock / avg_daily_sales_7d
- Message: `Остатки: "{sku_name}" — осталось на {days} дней ({stock} шт)`

### 2. Sales Drop
- Trigger: today sales < avg_7d * (1 - seller.alert_sales_drop_pct/100)
- Message: `Продажи: "{sku_name}" упали на {pct}% к среднему за 7 дней`

### 3. Unanswered Review
- Trigger: review age > seller.alert_review_hours (default 24h)
- Message: `Отзыв без ответа ({hours}ч): "{review_text_preview}..."`

---

## Service Interfaces (Protocol)

Both mock and real API clients implement the same interface:

```python
from typing import Protocol
from dataclasses import dataclass

@dataclass
class OrderSummary:
    date: str               # "2026-03-10"
    total_orders: int
    total_revenue: float    # in rubles
    total_returns: int

@dataclass
class StockItem:
    sku_id: str
    name: str
    current_stock: int
    avg_daily_sales_7d: float
    estimated_days_left: float

@dataclass
class Review:
    review_id: str
    sku_id: str
    sku_name: str
    rating: int             # 1-5
    text: str
    created_at: str         # ISO datetime
    is_answered: bool

@dataclass
class SalesAnomaly:
    sku_id: str
    name: str
    today_sales: int
    avg_7d_sales: float
    drop_pct: float


class MarketplaceClient(Protocol):
    async def get_order_summary(self, date: str) -> OrderSummary: ...
    async def get_stock_items(self) -> list[StockItem]: ...
    async def get_unanswered_reviews(self) -> list[Review]: ...
    async def get_sales_anomalies(self, threshold_pct: float) -> list[SalesAnomaly]: ...
    async def validate_token(self) -> bool: ...
```

`mock_api.py`, `ozon_api.py`, `wb_api.py` all implement `MarketplaceClient`.

---

## Ozon API Endpoints (MVP)

| Need | Endpoint | Method |
|------|----------|--------|
| Validate token | /v2/product/list | POST (limit=1) |
| Product list | /v2/product/list | POST |
| Stock levels | /v1/product/info/stocks | POST |
| Sales analytics | /v1/analytics/data | POST |
| Reviews | /v1/review/list | POST |

Auth: `Client-Id` + `Api-Key` headers on every request.

---

## WB API Endpoints (MVP)

| Need | Endpoint | Method |
|------|----------|--------|
| Validate token | /api/v3/orders | GET (limit=1) |
| Orders/sales | /api/v1/supplier/sales | GET |
| Stock levels | /api/v3/stocks/{warehouseId} | POST |
| Reviews | /feedbacks/v2/list | GET |

Auth: `Authorization: Bearer {token}` header.

---

## AI Reply Drafts

When bot shows an unanswered review:

```
Новый отзыв (2 звезды):
"Пришло мятое, упаковка ужасная, разочарован"

Черновик ответа:
"Добрый день! Приносим извинения за качество упаковки.
Мы уже усилили контроль на этапе сборки. Будем рады,
если дадите нам шанс исправить впечатление."

[Отправить] [Редактировать] [Пропустить]
```

Grok prompt for draft generation:

```
System: You write short, professional seller responses to marketplace reviews in Russian.
Rules:
- Max 3 sentences
- Apologize if negative, thank if positive
- Never argue with the buyer
- Sound human, not corporate
- Russian language only

User: Review ({rating} stars): "{review_text}"
Product: "{product_name}"
Write a response.
```

---

## V1 vs V2 Split

### V1 (MVP)
- Single owner per bot chat
- Ozon + WB via personal token
- Daily digest at fixed time
- 3 alert types
- AI draft replies (Grok)
- SQLite storage
- Render hosting

### V2 (after first paying clients)
- Manager role + shared group
- Configurable digest time
- Reply sending through marketplace API
- Multiple stores per owner
- Payment integration
- WB Solutions Catalog registration
- Analytics history / trends
