import bus
from domain.events import UserMessageEvent, CommandEvent
from typing import Type, Callable, Awaitable, Dict
import logging
from api.response import answer_to_user


Handler = Callable[[object, object], Awaitable[None]]  # Просто типизация на любую функцию
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
    logging.info(f"Calling the system when message{event} has been got")

    answer_to_user()

async def dispatcher(application):
    """
    Сам цикл с вызовами основных функций
    """
    while True:
        event = await bus.get()
        handler = HANDLERS.get(type(event)) # Получаем саму функцию, которая обрабатывает этот ивент

        if handler is None: # Если нет обработчика на такой случай (например на комманду)
            # TODO тоже логануть
            logging.info(f"for {event} there is no handler.")
            bus.task_done()  # То закрываем задачу
            continue

        await handler(event, application) # Вызываем эту функцию
        bus.task_done()  # Завершаем эту задачу
