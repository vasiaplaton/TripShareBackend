from typing import List, Optional
from pydantic import BaseModel


class ChatBase(BaseModel):
    user_id_1: int
    user_id_2: int


class ChatCreate(ChatBase):
    pass


class Chat(ChatBase):
    id: int


class ChatMessageBase(BaseModel):
    text: Optional[str] = None
    image_id: Optional[int] = None


class ChatMessageCreate(ChatMessageBase):
    pass


class ChatMessage(ChatMessageBase):
    id: int
    sender_id: int
    chat_id: int
