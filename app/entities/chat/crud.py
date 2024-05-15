from sqlalchemy import or_

from app.database import SessionLocal
from app.entities.chat import models, schemas
from app.entities.user.models import User


class ChatCRUD:
    def __init__(self, db: SessionLocal):
        self.db = db

    def get_chats_by_user_id(self, user_id: int) -> list[models.Chat]:
        return self.db.query(models.Chat).filter((models.Chat.user_id_1 == user_id) | (models.Chat.user_id_2 == user_id)).all()

    def create_chat(self, chat: schemas.ChatCreate) -> models.Chat:
        db_chat = models.Chat(**chat.dict())
        self.db.add(db_chat)
        self.db.commit()
        self.db.refresh(db_chat)
        return db_chat

    def get_messages_by_chat_id(self, chat_id: int) -> list[models.ChatMessage]:
        return self.db.query(models.ChatMessage).filter(models.ChatMessage.chat_id == chat_id).all()

    def find_or_create_chat(self, sender_id: int, receiver_id: int) -> models.Chat:
        chat = self.db.query(models.Chat).filter(
            or_(
                (models.Chat.user_id_1 == sender_id) & (models.Chat.user_id_2 == receiver_id),
                (models.Chat.user_id_1 == receiver_id) & (models.Chat.user_id_2 == sender_id)
            )
        ).first()
        if not chat:
            # Create a new chat if it doesn't exist
            chat = self.create_chat(schemas.ChatCreate(user_id_1=sender_id, user_id_2=receiver_id))
        return chat

    def create_message(self, message: schemas.ChatMessageCreate, sender_id: int, receiver_id: int) -> models.ChatMessage:
        user1 = self.db.query(User).get(sender_id)
        if not user1:
            raise ValueError("Sender with id {} not found".format(sender_id))

        user1 = self.db.query(User).get(receiver_id)
        if not user1:
            raise ValueError("Receiver with id {} not found".format(receiver_id))

        # Find or create chat
        chat = self.find_or_create_chat(sender_id, receiver_id)

        # Create message
        db_message = models.ChatMessage(**message.dict(), chat_id=chat.id, sender_id=sender_id)
        self.db.add(db_message)
        self.db.commit()
        self.db.refresh(db_message)
        return db_message