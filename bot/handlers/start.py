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
from bot.services.ozon_api import OzonApiClient
from bot.services.wb_api import WildberriesApiClient


def _marketplace_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Ozon", callback_data="onboarding:ozon"),
                InlineKeyboardButton("Wildberries", callback_data="onboarding:wb"),
            ],
            [InlineKeyboardButton("Демо", callback_data="onboarding:demo")],
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
        "Привет. Я помогу следить за магазином в Ozon и Wildberries.\n\n"
        "Выберите площадку для подключения."
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
            marketplace="ozon",
            display_name="Демо Ozon",
            connection_mode="mock",
            status="connected",
            credentials=None,
            use_mock=True,
        )
        database.upsert_marketplace_account(
            chat_id=update.effective_chat.id,
            marketplace="wb",
            display_name="Демо Wildberries",
            connection_mode="mock",
            status="connected",
            credentials=None,
            use_mock=True,
        )
        database.clear_onboarding_session(update.effective_chat.id)
        await update.callback_query.edit_message_text(
            "Демо-режим включен.\n\n"
            "Теперь доступны команды:\n"
            "/digest - демо-дайджест\n"
            "/reviews - отзывы без ответа\n"
            "/alerts - пороги алертов\n"
            "/status - статус подключений"
        )
        return

    if marketplace == "ozon":
        database.upsert_onboarding_session(
            chat_id=update.effective_chat.id,
            state="enter_ozon_credentials",
            selected_marketplace="ozon",
        )
        await update.callback_query.edit_message_text(
            "Отправьте `Client ID` и `API key` Ozon одним сообщением.\n"
            "Можно через пробел или с новой строки.",
            parse_mode="Markdown",
        )
        return

    if marketplace == "wb":
        database.upsert_onboarding_session(
            chat_id=update.effective_chat.id,
            state="enter_wb_token",
            selected_marketplace="wb",
        )
        await update.callback_query.edit_message_text(
            "Отправьте личный токен Wildberries одним сообщением.\n"
            "Для пилота используем данные только вашего кабинета."
        )


def _parse_ozon_credentials(text: str) -> tuple[str, str] | None:
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

    if session.state == "enter_ozon_credentials":
        credentials = _parse_ozon_credentials(update.message.text or "")
        if credentials is None:
            await update.message.reply_text(
                "Не смогла разобрать данные.\n"
                "Отправьте `Client ID` и `API key` через пробел или с новой строки.",
                parse_mode="Markdown",
            )
            return

        client_id, api_key = credentials
        ozon_api_client: OzonApiClient = context.application.bot_data["ozon_api_client"]
        database.upsert_marketplace_account(
            chat_id=update.effective_chat.id,
            marketplace="ozon",
            display_name="Ozon",
            connection_mode="api",
            status="pending",
            credentials={"client_id": client_id, "api_key": api_key},
            use_mock=False,
        )
        await update.message.reply_text("Проверяю подключение к Ozon API...")
        result = await ozon_api_client.validate_credentials(client_id=client_id, api_key=api_key)
        if result.is_valid:
            database.mark_marketplace_account_validation(
                chat_id=update.effective_chat.id,
                marketplace="ozon",
                status="connected",
                display_name=result.account_name or "Ozon",
                error_text=None,
            )
            database.clear_onboarding_session(update.effective_chat.id)
            await update.message.reply_text(
                "Ozon подключен.\n"
                "Подключение подтверждено, аккаунт сохранен.\n\n"
                "Команды:\n"
                "/status - статус подключения\n"
                "/digest - пока демо-формат\n"
                "/reviews - пока демо-формат"
            )
            return

        database.mark_marketplace_account_validation(
            chat_id=update.effective_chat.id,
            marketplace="ozon",
            status="invalid",
            error_text=result.error_text,
        )
        await update.message.reply_text(
            "Не удалось подтвердить Ozon API.\n"
            f"Причина: {result.error_text or 'неизвестная ошибка'}\n\n"
            "Проверьте данные и отправьте их заново."
        )
        return

    if session.state == "enter_wb_token":
        token = (update.message.text or "").strip()
        if not token:
            await update.message.reply_text("Отправьте непустой токен Wildberries.")
            return

        wb_api_client: WildberriesApiClient = context.application.bot_data["wb_api_client"]
        database.upsert_marketplace_account(
            chat_id=update.effective_chat.id,
            marketplace="wb",
            display_name="Wildberries",
            connection_mode="api",
            status="pending",
            credentials={"token": token},
            use_mock=False,
        )
        await update.message.reply_text("Проверяю подключение к Wildberries API...")
        result = await wb_api_client.validate_credentials(token=token)
        if result.is_valid:
            database.mark_marketplace_account_validation(
                chat_id=update.effective_chat.id,
                marketplace="wb",
                status="connected",
                display_name=result.account_name or "Wildberries",
                error_text=None,
            )
            database.clear_onboarding_session(update.effective_chat.id)
            await update.message.reply_text(
                "Wildberries подключен.\n"
                "Для пилота используем ваш личный токен и данные вашего кабинета.\n\n"
                "Команды:\n"
                "/status - статус подключения\n"
                "/digest - пока демо-формат\n"
                "/reviews - пока демо-формат"
            )
            return

        database.mark_marketplace_account_validation(
            chat_id=update.effective_chat.id,
            marketplace="wb",
            status="invalid",
            error_text=result.error_text,
        )
        await update.message.reply_text(
            "Не удалось подтвердить токен Wildberries.\n"
            f"Причина: {result.error_text or 'неизвестная ошибка'}\n\n"
            "Проверьте токен и отправьте его заново."
        )


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat is None or update.message is None:
        return

    database: Database = context.application.bot_data["database"]
    accounts = database.list_marketplace_accounts(chat_id=update.effective_chat.id)
    if not accounts:
        await update.message.reply_text("Подключений пока нет. Используйте /start.")
        return

    lines = ["Текущие подключения:"]
    for account in accounts:
        mode = "демо" if account.use_mock else "api"
        suffix = f", ошибка: {account.last_error_text}" if account.last_error_text else ""
        lines.append(f"- {account.display_name}: статус {account.status}, режим {mode}{suffix}")
    await update.message.reply_text("\n".join(lines))


def register_start_handlers(application: Application) -> None:
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CallbackQueryHandler(onboarding_callback, pattern=r"^onboarding:"))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, onboarding_text_input)
    )
