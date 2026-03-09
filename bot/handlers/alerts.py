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
        "Текущие пороги алертов:\n"
        f"- Остаток меньше: {settings.stock_days_threshold} дн.\n"
        f"- Падение продаж больше: {settings.sales_drop_percent_threshold}%\n"
        f"- Отзыв без ответа старше: {settings.review_age_hours_threshold} ч.\n"
        f"- Ежедневный дайджест: {'включен' if settings.digest_enabled else 'выключен'}\n"
        f"- Алерты: {'включены' if settings.alerts_enabled else 'выключены'}"
    )
    await update.message.reply_text(message)


def register_alert_handlers(application: Application) -> None:
    application.add_handler(CommandHandler("alerts", alerts_command))
