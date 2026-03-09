from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AlertSettings:
    chat_id: int
    stock_days_threshold: int
    sales_drop_percent_threshold: int
    review_age_hours_threshold: int
    digest_enabled: bool
    alerts_enabled: bool


@dataclass(frozen=True, slots=True)
class OnboardingSession:
    chat_id: int
    state: str
    selected_marketplace: str | None
    payload_json: str | None


@dataclass(frozen=True, slots=True)
class MarketplaceAccount:
    chat_id: int
    marketplace: str
    display_name: str
    connection_mode: str
    status: str
    credentials_json: str | None
    use_mock: bool
    last_validated_at: str | None
    last_error_text: str | None
