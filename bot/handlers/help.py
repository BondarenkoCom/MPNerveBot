from __future__ import annotations

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        return

    message = (
        "Available commands:\n"
        "/start - connect a marketplace account or enable demo mode\n"
        "/digest - view the sample daily digest\n"
        "/reviews - view sample unanswered reviews\n"
        "/alerts - show current alert thresholds\n"
        "/status - show saved connection status"
    )
    await update.message.reply_text(message)


def register_help_handlers(application: Application) -> None:
    application.add_handler(CommandHandler("help", help_command))
