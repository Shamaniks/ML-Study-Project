from .dispatcher import register
from domain.events import UserMessageEvent
from handlers.answer_handler import handle_user_message_model

# register(UserMessageEvent, handle_user_message_model)
