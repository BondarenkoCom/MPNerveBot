from __future__ import annotations

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        return

    message = (
        "Доступные команды:\n"
        "/start - начать подключение или включить демо\n"
        "/digest - демо-дайджест за сегодня\n"
        "/reviews - список неотвеченных отзывов\n"
        "/alerts - текущие настройки алертов\n"
        "/status - статус подключений"
    )
    await update.message.reply_text(message)


def register_help_handlers(application: Application) -> None:
    application.add_handler(CommandHandler("help", help_command))
