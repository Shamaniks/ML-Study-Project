from telegram import Update # Для типизации

from ._queue import put, get, task_done
from domain.events import UserMessageEvent, CommandEvent

async def put_message(update: Update):
    event = UserMessageEvent(
        chat_id=update.message.chat_id,
        user_id=update.message.user_id,
        text   =update.message.text,
    )
    await put(event)

async def put_command(update: Update):
    event = CommandEvent(
        chat_id=update.message.chat_id,
        user_id=update.message.user_id,
        command=update.message.text,
    )
    await put(event)

# Фокусы с импортами
__all__ = ["put_message", "put_command", "get", "task_done"]
