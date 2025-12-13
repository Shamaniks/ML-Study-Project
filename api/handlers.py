from telegram import Update
from telegram.ext import ContextTypes
import bus

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # TODO
    # Залогировать старт бота
    print("Стартанул")

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update.message.text)
    await bus.put_message(update)
    # TODO Тоже залогировать
