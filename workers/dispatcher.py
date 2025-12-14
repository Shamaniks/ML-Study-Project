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

async def dispatcher(application):
    """
    Сам цикл с вызовами основных функций
    """
    while True:
        event = await bus.get()
        handler = HANDLERS.get(type(event), handle_unknown) # Получаем саму функцию, которая обрабатывает этот ивент
        await handler(event, application) # Вызываем эту функцию
        bus.task_done()  # Завершаем эту задачу
