from dispatcher import register
from dispatcher import handle_user_message
from domain.events import UserMessageEvent

register(UserMessageEvent, handle_user_message)
