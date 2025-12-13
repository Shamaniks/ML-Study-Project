import bus
from domain.events import UserMessageEvent, CommandEvent
from typing import Type, Callable, Awaitable, Dict

Handler = Callable[[object, object], Awaitable[None]] # Просто типизация на любую функцию
HANDLERS: Dict[Type, Handler] = {}

def register(event_type: Type, handler: Handler):
    """
    Регистрация обработки при разных ситуациях. Вызывается в workers/__init__.py
    Нужен, потому что я не хочу просто двигать его после объявлений функций
    """
    HANDLERS[event_type] = handler

async def handle_user_message(event: UserMessageEvent, application):
    """
    Здесь происходит вызов логики при получении сообщения
    """
    await application.bot.send_message(
        chat_id=event.chat_id,
        text=event.text.upper()
    )
