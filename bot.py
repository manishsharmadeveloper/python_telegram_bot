
import os
import logging

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    await update.message.reply_text(
        "Hello! Welcome to my Python Telegram bot.\n\n"
        "Available commands:\n"
        "/start - Start the bot\n"
        "/help - Show help\n"
        "/about - About this bot\n\n"
        "Send me any text and I will repeat it."
    )


async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    await update.message.reply_text(
        "How to use this bot:\n"
        "/start - Start the bot\n"
        "/help - Display help\n"
        "/about - Bot information\n\n"
        "You can also send a normal text message."
    )


async def about(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    await update.message.reply_text(
        "I am a Telegram bot built with Python "
        "and the python-telegram-bot library."
    )


async def echo(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if update.message and update.message.text:
        await update.message.reply_text(update.message.text)


async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE,
):
    logger.error(
        "An error occurred while processing an update",
        exc_info=context.error,
    )


def main():
    if not TOKEN:
        raise RuntimeError(
            "TELEGRAM_BOT_TOKEN is missing from your .env file."
        )

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, echo)
    )

    app.add_error_handler(error_handler)

    logger.info("Python Telegram bot is starting...")
    app.run_polling()


if __name__ == "__main__":
    main()
