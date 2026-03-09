from telegram.ext import Application

from bot.handlers.alerts import register_alert_handlers
from bot.handlers.digest import register_digest_handlers
from bot.handlers.help import register_help_handlers
from bot.handlers.reviews import register_review_handlers
from bot.handlers.start import register_start_handlers


def register_handlers(application: Application) -> None:
    register_start_handlers(application)
    register_help_handlers(application)
    register_digest_handlers(application)
    register_alert_handlers(application)
    register_review_handlers(application)
