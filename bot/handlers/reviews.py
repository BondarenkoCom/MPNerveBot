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
            "A real account is connected, but this public showcase still uses sample review data.\n"
            "Showing demo content so the interaction flow can be reviewed."
        )

    reviews = mock_client.get_unanswered_reviews(chat_id=update.effective_chat.id, marketplace="demo")

    lines = ["Unanswered reviews:"]
    for review in reviews[:5]:
        lines.append(
            f"- {review.product_name} | {review.rating}/5 | {review.age_hours}h ago\n"
            f"  {review.text}"
        )

    await update.message.reply_text("\n".join(lines))


def register_review_handlers(application: Application) -> None:
    application.add_handler(CommandHandler("reviews", reviews_command))
