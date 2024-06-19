from typing import Optional

from app.database import models
from app.database.database import SessionLocal
from app.entities.pays import schemas


def _model_to_schema(db_item: models.Pay) -> Optional[schemas.PayReturn]:
    if db_item is None:
        return None
    return schemas.PayReturn.model_validate(db_item.__dict__)


def _models_to_schema(db_items: list[models.Place]) -> list[schemas.PayReturn]:
    return [_model_to_schema(db_item) for db_item in db_items]


class PaysCrud:
    def __init__(self, db: SessionLocal):
        self.db = db

    def create(self, schema: schemas.Pay, commit: bool = True) -> models.Place:
        db_entity = models.Pay(
            **schema.dict(),
        )

        self.db.add(db_entity)
        if commit:
            self.db.commit()
        else:
            self.db.flush()

        self.db.refresh(db_entity)

        return db_entity

    def get_for_me(self):
        self.db.query(models.Place).filter(models.Place.id == id).first()
