from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True, slots=True)
class Settings:
    telegram_bot_token: str
    telegram_admin_chat_id: int | None
    xai_api_key: str | None
    openai_api_key: str | None
    app_env: str
    app_base_url: str | None
    webhook_secret: str | None
    database_path: Path
    timezone_name: str
    digest_hour_moscow: int
    alert_interval_hours: int
    app_mode: str
    ozon_real_enabled: bool
    wb_real_enabled: bool


def _env_flag(name: str, default: bool) -> bool:
    raw_value = os.getenv(name)
    if raw_value is None:
        return default
    return raw_value.strip().lower() in {"1", "true", "yes", "on"}


def load_settings() -> Settings:
    base_dir = Path(__file__).resolve().parents[1]
    load_dotenv(base_dir / ".env")

    data_dir = base_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    database_path = Path(os.getenv("DATABASE_PATH", data_dir / "mpnervebot.sqlite3"))
    if not database_path.is_absolute():
        database_path = base_dir / database_path

    telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    if not telegram_bot_token:
        raise ValueError("TELEGRAM_BOT_TOKEN is required")

    admin_chat_id = os.getenv("TELEGRAM_ADMIN_CHAT_ID", "").strip()

    return Settings(
        telegram_bot_token=telegram_bot_token,
        telegram_admin_chat_id=int(admin_chat_id) if admin_chat_id else None,
        xai_api_key=os.getenv("XAI_API_KEY"),
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        app_env=os.getenv("APP_ENV", "development"),
        app_base_url=os.getenv("APP_BASE_URL"),
        webhook_secret=os.getenv("WEBHOOK_SECRET"),
        database_path=database_path,
        timezone_name=os.getenv("TIMEZONE_NAME", "Europe/Moscow"),
        digest_hour_moscow=int(os.getenv("DIGEST_HOUR_MOSCOW", "9")),
        alert_interval_hours=int(os.getenv("ALERT_INTERVAL_HOURS", "2")),
        app_mode=os.getenv("APP_MODE", "demo"),
        ozon_real_enabled=_env_flag("OZON_REAL_ENABLED", False),
        wb_real_enabled=_env_flag("WB_REAL_ENABLED", False),
    )
