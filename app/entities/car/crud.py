from typing import Optional

from app.database import models
from app.database.database import SessionLocal
from app.entities.car import schemas
from app.entities.exceptions import NotFound


def _model_to_schema(db_item: models.Car) -> Optional[schemas.CarReturn]:
    if db_item is None:
        return None
    return schemas.CarReturn.model_validate(db_item.__dict__)


def _models_to_schema(db_items: list[models.Car]) -> list[schemas.CarReturn]:
    return [_model_to_schema(db_item) for db_item in db_items]


class CarCrud:
    def __init__(self, db: SessionLocal):
        self.db = db

    def create(self, schema: schemas.CarCreate, commit: bool = True) -> models.Car:
        db_entity = models.Car(
            **schema.dict(),
        )

        self.db.add(db_entity)
        if commit:
            self.db.commit()
        else:
            self.db.flush()

        self.db.refresh(db_entity)

        return db_entity

    def get_by_id(self, id: int) -> models.Car:
        return self.db.query(models.Car).filter(models.Car.id == id).all()

    def get_by_user_id(self, user_id: int) -> models.Car:
        return self.db.query(models.Car).filter(models.Car.user_id == user_id).all()

    def delete(self, id: int, commit: bool = True):
        res = self.db.query(models.Car).filter(
            models.Car.id == id).first()
        if res is None:
            raise NotFound
        res.delete()
        if commit:
            self.db.commit()
        else:
            self.db.flush()
