from __future__ import annotations

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from bot.models.db import Database
from bot.services.marketplace_a_api import MarketplaceAApiClient
from bot.services.marketplace_b_api import MarketplaceBApiClient


def _marketplace_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Marketplace A", callback_data="onboarding:marketplace_a"),
            ],
            [
                InlineKeyboardButton("Marketplace B", callback_data="onboarding:marketplace_b"),
            ],
            [InlineKeyboardButton("Demo", callback_data="onboarding:demo")],
        ]
    )


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user is None or update.effective_chat is None or update.message is None:
        return

    database: Database = context.application.bot_data["database"]
    database.upsert_telegram_user(
        telegram_user_id=update.effective_user.id,
        chat_id=update.effective_chat.id,
        username=update.effective_user.username,
        first_name=update.effective_user.first_name,
        last_name=update.effective_user.last_name,
    )
    database.upsert_onboarding_session(
        chat_id=update.effective_chat.id,
        state="choose_marketplace",
    )

    message = (
        "Welcome. This bot demonstrates a Telegram-first marketplace operations workflow.\n\n"
        "Choose a connection type to continue."
    )
    await update.message.reply_text(message, reply_markup=_marketplace_keyboard())


async def onboarding_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.callback_query is None or update.effective_chat is None:
        return

    database: Database = context.application.bot_data["database"]
    marketplace = update.callback_query.data.removeprefix("onboarding:")
    await update.callback_query.answer()

    if marketplace == "demo":
        database.upsert_marketplace_account(
            chat_id=update.effective_chat.id,
            marketplace="marketplace_a",
            display_name="Demo Marketplace A",
            connection_mode="mock",
            status="connected",
            credentials=None,
            use_mock=True,
        )
        database.upsert_marketplace_account(
            chat_id=update.effective_chat.id,
            marketplace="marketplace_b",
            display_name="Demo Marketplace B",
            connection_mode="mock",
            status="connected",
            credentials=None,
            use_mock=True,
        )
        database.clear_onboarding_session(update.effective_chat.id)
        await update.callback_query.edit_message_text(
            "Demo mode is enabled.\n\n"
            "Available commands:\n"
            "/digest - sample daily digest\n"
            "/reviews - sample unanswered reviews\n"
            "/alerts - current alert thresholds\n"
            "/status - connection status"
        )
        return

    if marketplace == "marketplace_a":
        database.upsert_onboarding_session(
            chat_id=update.effective_chat.id,
            state="enter_marketplace_a_credentials",
            selected_marketplace="marketplace_a",
        )
        await update.callback_query.edit_message_text(
            "Send the `Account ID` and `Access Key` for Marketplace A in one message.\n"
            "You can separate them with a space or a newline.",
            parse_mode="Markdown",
        )
        return

    if marketplace == "marketplace_b":
        database.upsert_onboarding_session(
            chat_id=update.effective_chat.id,
            state="enter_marketplace_b_credentials",
            selected_marketplace="marketplace_b",
        )
        await update.callback_query.edit_message_text(
            "Send the `Access Token` for Marketplace B in one message.",
            parse_mode="Markdown",
        )


def _parse_marketplace_a_credentials(text: str) -> tuple[str, str] | None:
    parts = [item.strip() for item in text.replace("\r", "\n").splitlines() if item.strip()]
    if len(parts) == 1:
        compact = parts[0].split()
        if len(compact) != 2:
            return None
        return compact[0], compact[1]
    if len(parts) >= 2:
        return parts[0], parts[1]
    return None


async def onboarding_text_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat is None or update.message is None:
        return

    database: Database = context.application.bot_data["database"]
    session = database.get_onboarding_session(chat_id=update.effective_chat.id)
    if session is None:
        return

    if session.state == "enter_marketplace_a_credentials":
        credentials = _parse_marketplace_a_credentials(update.message.text or "")
        if credentials is None:
            await update.message.reply_text(
                "Could not parse the credentials.\n"
                "Send `Account ID` and `Access Key` separated by a space or newline.",
                parse_mode="Markdown",
            )
            return

        account_id, access_key = credentials
        marketplace_a_api_client: MarketplaceAApiClient = context.application.bot_data["marketplace_a_api_client"]
        database.upsert_marketplace_account(
            chat_id=update.effective_chat.id,
            marketplace="marketplace_a",
            display_name="Marketplace A",
            connection_mode="api",
            status="pending",
            credentials={"account_id": account_id, "access_key": access_key},
            use_mock=False,
        )
        await update.message.reply_text("Validating Marketplace A credentials...")
        result = await marketplace_a_api_client.validate_credentials(
            account_id=account_id,
            access_key=access_key,
        )
        if result.is_valid:
            database.mark_marketplace_account_validation(
                chat_id=update.effective_chat.id,
                marketplace="marketplace_a",
                status="connected",
                display_name=result.account_name or "Marketplace A",
                error_text=None,
            )
            database.clear_onboarding_session(update.effective_chat.id)
            await update.message.reply_text(
                "Marketplace A is connected.\n"
                "The account has been validated and saved.\n\n"
                "Commands:\n"
                "/status - connection status\n"
                "/digest - sample digest format\n"
                "/reviews - sample review format"
            )
            return

        database.mark_marketplace_account_validation(
            chat_id=update.effective_chat.id,
            marketplace="marketplace_a",
            status="invalid",
            error_text=result.error_text,
        )
        await update.message.reply_text(
            "Marketplace A validation failed.\n"
            f"Reason: {result.error_text or 'unknown error'}\n\n"
            "Check the credentials and send them again."
        )
        return

    if session.state == "enter_marketplace_b_credentials":
        token = (update.message.text or "").strip()
        if not token:
            await update.message.reply_text("Send a non-empty Marketplace B access token.")
            return

        marketplace_b_api_client: MarketplaceBApiClient = context.application.bot_data["marketplace_b_api_client"]
        database.upsert_marketplace_account(
            chat_id=update.effective_chat.id,
            marketplace="marketplace_b",
            display_name="Marketplace B",
            connection_mode="api",
            status="pending",
            credentials={"token": token},
            use_mock=False,
        )
        await update.message.reply_text("Validating Marketplace B access token...")
        result = await marketplace_b_api_client.validate_credentials(access_token=token)
        if result.is_valid:
            database.mark_marketplace_account_validation(
                chat_id=update.effective_chat.id,
                marketplace="marketplace_b",
                status="connected",
                display_name=result.account_name or "Marketplace B",
                error_text=None,
            )
            database.clear_onboarding_session(update.effective_chat.id)
            await update.message.reply_text(
                "Marketplace B is connected.\n"
                "The account has been validated and saved.\n\n"
                "Commands:\n"
                "/status - connection status\n"
                "/digest - sample digest format\n"
                "/reviews - sample review format"
            )
            return

        database.mark_marketplace_account_validation(
            chat_id=update.effective_chat.id,
            marketplace="marketplace_b",
            status="invalid",
            error_text=result.error_text,
        )
        await update.message.reply_text(
            "Marketplace B validation failed.\n"
            f"Reason: {result.error_text or 'unknown error'}\n\n"
            "Check the token and send it again."
        )


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat is None or update.message is None:
        return

    database: Database = context.application.bot_data["database"]
    accounts = database.list_marketplace_accounts(chat_id=update.effective_chat.id)
    if not accounts:
        await update.message.reply_text("No connections saved yet. Use /start.")
        return

    lines = ["Current connections:"]
    for account in accounts:
        mode = "demo" if account.use_mock else "api"
        suffix = f", error: {account.last_error_text}" if account.last_error_text else ""
        lines.append(f"- {account.display_name}: status {account.status}, mode {mode}{suffix}")
    await update.message.reply_text("\n".join(lines))


def register_start_handlers(application: Application) -> None:
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CallbackQueryHandler(onboarding_callback, pattern=r"^onboarding:"))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, onboarding_text_input)
    )
