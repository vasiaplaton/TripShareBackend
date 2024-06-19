from operator import or_
from typing import Optional

from app.database import models
from app.database.database import SessionLocal
from app.entities.enums import PaymentStatus
from app.entities.exceptions import NotFound
from app.entities.pays import schemas


def _model_to_schema(db_item: models.Pay) -> Optional[schemas.PayReturn]:
    if db_item is None:
        return None
    return schemas.PayReturn.model_validate(db_item.__dict__)


def _models_to_schema(db_items: list[models.Pay]) -> list[schemas.PayReturn]:
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

    def get_for_id(self, id: int) -> models.Pay:
        return self.db.query(models.Pay).filter(models.Pay.id == id).first()

    def get_for_request(self, request_id: int) -> models.Pay:
        return self.db.query(models.Pay).filter(models.Pay.request_id == request_id).first()

    def update_status(self, id, status: PaymentStatus, commit: bool = True):
        db_entity = self.get_for_id(id)
        if db_entity is None:
            return NotFound()

        db_entity.status = status

        if commit:
            self.db.commit()
        else:
            self.db.flush()

        self.db.refresh(db_entity)

        return db_entity

    def get_for_me(self, user_id: int) -> list[models.Pay]:
        return self.db.query(models.Pay).filter(
            or_(
                (models.Pay.to_user_id == user_id),
                (models.Pay.from_user_id == user_id)
            )
        ).all()
