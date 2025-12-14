from telegram import Update
from telegram.ext import ContextTypes
import bus
import logging

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("Bot started.")
    print("Стартанул")

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await bus.put_message(update)
