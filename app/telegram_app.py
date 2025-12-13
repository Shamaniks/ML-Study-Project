from telegram.ext import Application, CommandHandler, MessageHandler, filters

from api.handlers import start, message_handler
from app.lifecycle import on_startup

def build(token: str):
    app = Application.builder().token(token).post_init(on_startup).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    return app
