from typing import Optional

from app.database import models
from app.database.database import SessionLocal
from app.entities.trip import schemas


def _model_to_schema(db_item: models.Stop) -> Optional[schemas.StopReturn]:
    if db_item is None:
        return None
    return schemas.StopReturn.model_validate(db_item.__dict__)


def _models_to_schema(db_items: list[models.Stop]) -> list[schemas.StopReturn]:
    return [_model_to_schema(db_item) for db_item in db_items]


class StopCrud:
    def __init__(self, db: SessionLocal):
        self.db = db

    def get_stops_by_trip_id(self, trip_id: int) -> list[models.Chat]:
        return self.db.query(models.Stop).filter(models.Stop.trip_id == trip_id).all()

    def create(self,
               schema: schemas.Stop,
               trip_id: int,
               is_start: bool,
               is_stop: bool,
               commit: bool = True) -> models.Chat:

        db_entity = models.Stop(
            **schema.model_dump(),
            trip_id=trip_id,
            is_start=is_start,
            is_stop=is_stop
        )

        self.db.add(db_entity)
        if commit:
            self.db.commit()
        else:
            self.db.flush()

        self.db.refresh(db_entity)

        return db_entity
