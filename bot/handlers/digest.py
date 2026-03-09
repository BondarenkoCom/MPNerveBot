from __future__ import annotations

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from bot.models.db import Database
from bot.services.mock_api import MockMarketplaceClient
from bot.services.schemas import DailyDigest


def _format_digest(payload: DailyDigest) -> str:
    stock_lines = "\n".join(
        f"- {item.product_name}: approximately {item.days_left} days of stock left"
        for item in payload.stock_risks
    )
    review_line = (
        f"Unanswered reviews: {payload.unanswered_reviews_count}\n"
        f"Oldest review age: {payload.oldest_review_age_hours} hours"
    )
    anomaly_line = (
        f"{payload.top_anomaly.product_name}: sales down "
        f"{payload.top_anomaly.drop_percent}% vs 7-day average"
    )
    return (
        f"Daily digest for {payload.digest_date} ({payload.marketplace_label})\n\n"
        f"Orders: {payload.orders_count} ({payload.orders_delta_percent:+d}% vs yesterday)\n"
        f"Revenue: {payload.revenue_amount_rub:,}\n"
        f"Returns: {payload.returns_count}\n\n"
        f"Stock risks:\n{stock_lines}\n\n"
        f"{review_line}\n\n"
        f"Top anomaly:\n{anomaly_line}"
    )


async def digest_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat is None or update.message is None:
        return

    database: Database = context.application.bot_data["database"]
    mock_client: MockMarketplaceClient = context.application.bot_data["mock_client"]
    accounts = database.list_marketplace_accounts(chat_id=update.effective_chat.id)
    connected_real = [account for account in accounts if not account.use_mock and account.status == "connected"]

    if connected_real:
        await update.message.reply_text(
            "A real account is connected, but this public showcase still uses a sample digest format.\n"
            "Showing demo data so the UX can be reviewed."
        )
        marketplace_label = connected_real[0].display_name
    else:
        marketplace_label = "demo mode"

    payload = mock_client.get_daily_digest(chat_id=update.effective_chat.id, marketplace="demo")
    payload = DailyDigest(
        marketplace_label=marketplace_label,
        digest_date=payload.digest_date,
        orders_count=payload.orders_count,
        orders_delta_percent=payload.orders_delta_percent,
        revenue_amount_rub=payload.revenue_amount_rub,
        returns_count=payload.returns_count,
        stock_risks=payload.stock_risks,
        unanswered_reviews_count=payload.unanswered_reviews_count,
        oldest_review_age_hours=payload.oldest_review_age_hours,
        top_anomaly=payload.top_anomaly,
    )
    await update.message.reply_text(_format_digest(payload))


def register_digest_handlers(application: Application) -> None:
    application.add_handler(CommandHandler("digest", digest_command))
