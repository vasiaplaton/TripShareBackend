import datetime
from typing import Optional

from app.database import models
from app.database.database import SessionLocal
from app.entities.chats import schemas
from app.entities.chats.chat_crud import ChatCrud
from app.entities.user.crud import UserCrud


def _model_to_schema(db_item: models.ChatMessage) -> Optional[schemas.ChatMessageReturn]:
    if db_item is None:
        return None
    return schemas.ChatMessageReturn.model_validate(db_item.__dict__)


def _models_to_schema(db_items: list[models.ChatMessage]) -> list[schemas.ChatMessageReturn]:
    return [_model_to_schema(db_item) for db_item in db_items]


class ChatMessageCrud:
    def __init__(self, db: SessionLocal):
        self.db = db

    def send_message(self, message: schemas.ChatMessageCreate, sender_id: int, commit: bool = True):
        receiver_id = message.receiver_id

        user1 = UserCrud(self.db).get_user_by_id(sender_id)
        if not user1:
            raise ValueError("Sender with id {} not found".format(sender_id))

        user2 = UserCrud(self.db).get_user_by_id(receiver_id)
        if not user2:
            raise ValueError("Receiver with id {} not found".format(receiver_id))

        chat = ChatCrud(self.db).find_chat(sender_id, receiver_id)
        if not chat:
            chat = ChatCrud(self.db).create(schemas.ChatCreate(
                user_id_1=sender_id,
                user_id_2=receiver_id
            ), commit=commit)

        db_message = models.ChatMessage(**message.model_dump(exclude={"receiver_id"}),
                                        chat_id=chat.id,
                                        sender_id=sender_id,
                                        created_at=datetime.datetime.now()
                                        )

        self.db.add(db_message)
        if commit:
            self.db.commit()
        else:
            self.db.flush()
        self.db.refresh(db_message)
        return db_message

    def get_message_by_chat_id(self, chat_id: int):
        return self.db.query(models.ChatMessage).filter(models.ChatMessage.chat_id == chat_id).all()
