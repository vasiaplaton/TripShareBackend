import datetime
from typing import Optional

from sqlalchemy import or_
from app.entities.user import crud as user_crud
from app.database import models
from app.database.database import SessionLocal
from app.entities.chats import schemas


def _model_to_schema(db_item: models.Chat, db: SessionLocal, user_dto: bool = True) -> Optional[schemas.ChatReturn]:
    if db_item is None:
        return None
    d = db_item.__dict__

    if user_dto:
        d["user_1"] = user_crud._model_to_schema(user_crud.UserCrud(db).get_user_by_id(db_item.user_id_1), db,
                                                 car_dto=False)
        d["user_2"] = user_crud._model_to_schema(user_crud.UserCrud(db).get_user_by_id(db_item.user_id_2), db,
                                                 car_dto=False)
    return schemas.ChatReturn.model_validate(db_item.__dict__)


def _models_to_schema(db_items: list[models.Chat], db: SessionLocal, user_dto: bool = True) -> list[schemas.ChatReturn]:
    return [_model_to_schema(db_item, db, user_dto) for db_item in db_items]


class ChatCrud:
    def __init__(self, db: SessionLocal):
        self.db = db

    def get_chats_by_user_id(self, user_id: int) -> list[models.Chat]:
        return self.db.query(models.Chat).filter(
            (models.Chat.user_id_1 == user_id) | (models.Chat.user_id_2 == user_id)).all()

    def find_chat(self, user_id_1: int, user_id_2: int):
        return self.db.query(models.Chat).filter(
            or_(
                (models.Chat.user_id_1 == user_id_1) & (models.Chat.user_id_2 == user_id_2),
                (models.Chat.user_id_1 == user_id_2) & (models.Chat.user_id_2 == user_id_1)
            )
        ).first()

    def create(self, schema: schemas.ChatCreate, commit: bool = True) -> models.Chat:
        db_entity = models.Chat(
            **schema.model_dump(),
        )

        self.db.add(db_entity)
        if commit:
            self.db.commit()
        else:
            self.db.flush()

        self.db.refresh(db_entity)

        return db_entity


