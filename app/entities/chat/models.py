from sqlalchemy import ForeignKey, Column, Integer, String

from app.database import Base


class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True)

    user_id_1 = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
    user_id_2 = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True)

    text = Column(String, nullable=True)
    image_path = Column(String, nullable=True)

    sender_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
    chat_id = Column(Integer, ForeignKey("chats.id", ondelete='CASCADE'), nullable=False)
