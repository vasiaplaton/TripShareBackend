import datetime
from typing import Optional

from sqlalchemy import or_

from app.database import models
from app.database.database import SessionLocal
from app.entities.enums import RequestStatus
from app.entities.requests import schemas


def _model_to_schema(db_item: models.Chat) -> Optional[schemas.Request]:
    if db_item is None:
        return None
    return schemas.ChatReturn.model_validate(db_item.__dict__)


def _models_to_schema(db_items: list[models.Chat]) -> list[schemas.ChatReturn]:
    return [_model_to_schema(db_item) for db_item in db_items]


class RequestCrud:
    def __init__(self, db: SessionLocal):
        self.db = db

    def find_for_trip_id(self, trip_id: int) -> list[models.Request]:
        return self.db.query(models.Request).filter(models.Request.trip_id == trip_id).all()

    def find_for_trip_id_and_status(self, trip_id: int, status: RequestStatus) -> list[models.Request]:
        return (self.db.query(models.Request).
                filter(models.Request.trip_id == trip_id).
                filter(models.Request.status == status).all())
