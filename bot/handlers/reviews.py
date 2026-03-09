from __future__ import annotations

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from bot.models.db import Database
from bot.services.mock_api import MockMarketplaceClient


async def reviews_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat is None or update.message is None:
        return

    database: Database = context.application.bot_data["database"]
    mock_client: MockMarketplaceClient = context.application.bot_data["mock_client"]
    accounts = database.list_marketplace_accounts(chat_id=update.effective_chat.id)
    connected_real = [account for account in accounts if not account.use_mock and account.status == "connected"]

    if connected_real:
        await update.message.reply_text(
            "Реальное подключение подтверждено, но живой список отзывов еще не подключен.\n"
            "Пока показываю демо-формат, чтобы можно было проверить механику."
        )

    reviews = mock_client.get_unanswered_reviews(chat_id=update.effective_chat.id, marketplace="demo")

    lines = ["Отзывы без ответа:"]
    for review in reviews[:5]:
        lines.append(
            f"- {review.product_name} | {review.rating}/5 | {review.age_hours} ч.\n"
            f"  {review.text}"
        )

    await update.message.reply_text("\n".join(lines))


def register_review_handlers(application: Application) -> None:
    application.add_handler(CommandHandler("reviews", reviews_command))
