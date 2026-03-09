from __future__ import annotations

import logging
import os

from telegram.ext import Application

from bot.handlers import register_handlers
from bot.models.db import Database
from bot.services.marketplace_a_api import MarketplaceAApiClient
from bot.services.marketplace_b_api import MarketplaceBApiClient
from bot.services.mock_api import MockMarketplaceClient
from config.settings import Settings, load_settings


logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    level=logging.INFO,
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)


def build_application(settings: Settings) -> Application:
    database = Database(settings.database_path)
    database.initialize()

    application = Application.builder().token(settings.telegram_bot_token).build()
    application.bot_data["settings"] = settings
    application.bot_data["database"] = database
    application.bot_data["mock_client"] = MockMarketplaceClient()
    application.bot_data["marketplace_a_api_client"] = MarketplaceAApiClient()
    application.bot_data["marketplace_b_api_client"] = MarketplaceBApiClient()

    register_handlers(application)
    return application


def main() -> None:
    settings = load_settings()
    application = build_application(settings)

    if settings.app_base_url:
        port = int(os.getenv("PORT", "10000"))
        url_path = f"telegram/{settings.webhook_secret or 'webhook'}"
        webhook_url = f"{settings.app_base_url.rstrip('/')}/{url_path}"
        application.run_webhook(
            listen="0.0.0.0",
            port=port,
            url_path=url_path,
            webhook_url=webhook_url,
            secret_token=settings.webhook_secret,
            drop_pending_updates=True,
        )
        return

    application.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
