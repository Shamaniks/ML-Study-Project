from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # TODO
    # Залогировать старт бота
    pass

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await bus.put_message(update)
    # TODO Тоже залогировать
