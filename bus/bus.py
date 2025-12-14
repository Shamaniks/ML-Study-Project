from telegram import Update # Для типизации

from ._queue import put, get, task_done
from domain.events import UserMessageEvent, CommandEvent

async def put_message(update: Update):
    event = UserMessageEvent(
<<<<<<< HEAD
        chat_id=update.message.chat.id,
        user_id=update.message.from_user.id,
        text=update.message.text,
=======
        chat_id=update.message.chat_id,
        user_id=update.effective_user.id,  #update.message.user_id,
        text   =update.message.text,
>>>>>>> 8430e19 (Fix error w user id, add logging)
    )
    await put(event)

async def put_command(update: Update):
    event = CommandEvent(
<<<<<<< HEAD
        chat_id=update.message.chat.id,
        user_id=update.message.from_user.id,
=======
        chat_id=update.message.chat_id,
        user_id=update.effective_user.id,  #update.message.user_id,
>>>>>>> 8430e19 (Fix error w user id, add logging)
        command=update.message.text,
    )
    await put(event)

# Фокусы с импортами
__all__ = ["put_message", "put_command", "get", "task_done"]
