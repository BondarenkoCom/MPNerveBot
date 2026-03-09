from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class StockRisk:
    product_name: str
    days_left: int


@dataclass(frozen=True, slots=True)
class ReviewItem:
    review_id: str
    product_name: str
    rating: int
    text: str
    age_hours: int


@dataclass(frozen=True, slots=True)
class SalesAnomaly:
    product_name: str
    drop_percent: int


@dataclass(frozen=True, slots=True)
class DailyDigest:
    marketplace_label: str
    digest_date: str
    orders_count: int
    orders_delta_percent: int
    revenue_amount_rub: int
    returns_count: int
    stock_risks: list[StockRisk]
    unanswered_reviews_count: int
    oldest_review_age_hours: int
    top_anomaly: SalesAnomaly
