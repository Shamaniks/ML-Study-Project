from dataclasses import dataclass

@dataclass(frozen=True)
class UserMessageEvent:
    chat_id: int
    user_id: int
    text:    str

@dataclass(frozen=True)
class CommandEvent:
    chat_id: int
    user_id: int
    command: str
