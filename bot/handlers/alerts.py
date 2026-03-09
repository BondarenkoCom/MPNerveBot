from __future__ import annotations

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from bot.models.db import Database


async def alerts_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat is None or update.message is None:
        return

    database: Database = context.application.bot_data["database"]
    settings = database.get_or_create_alert_settings(chat_id=update.effective_chat.id)
    message = (
        "Current alert thresholds:\n"
        f"- Stock coverage below: {settings.stock_days_threshold} days\n"
        f"- Sales drop above: {settings.sales_drop_percent_threshold}%\n"
        f"- Review age above: {settings.review_age_hours_threshold} hours\n"
        f"- Daily digest: {'enabled' if settings.digest_enabled else 'disabled'}\n"
        f"- Alerts: {'enabled' if settings.alerts_enabled else 'disabled'}"
    )
    await update.message.reply_text(message)


def register_alert_handlers(application: Application) -> None:
    application.add_handler(CommandHandler("alerts", alerts_command))
