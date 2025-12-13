from telegram.ext import Application, CommandHandler, MessageHandler, filters
from api.handlers import start, message_handler

def build(token: str):
    app = Application.builder().token(token).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_gandler))
    return app
