from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.entities.user.schemas import UserReturn


class ChatCreate(BaseModel):
    user_id_1: int
    user_id_2: int


class ChatReturn(ChatCreate):
    id: int
    user_1: Optional[UserReturn] = None
    user_2: Optional[UserReturn] = None


class ChatMessage(BaseModel):
    text: str
    image_url: Optional[str] = None


class ChatMessageCreate(ChatMessage):
    receiver_id: int


class ChatMessageReturn(ChatMessage):
    id: int
    created_at: datetime
    sender_id: int
    chat_id: int
