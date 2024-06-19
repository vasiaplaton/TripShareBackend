from typing import Optional

from sqlalchemy import func

from app.database import models
from app.database.database import SessionLocal
from app.entities.places import schemas
from app.entities.exceptions import NotFound


def _model_to_schema(db_item: models.Place) -> Optional[schemas.PlaceReturn]:
    if db_item is None:
        return None
    return schemas.PlaceReturn.model_validate(db_item.__dict__)


def _models_to_schema(db_items: list[models.Place]) -> list[schemas.PlaceReturn]:
    return [_model_to_schema(db_item) for db_item in db_items]


class PlacesCrud:
    def __init__(self, db: SessionLocal):
        self.db = db

    def create(self, schema: schemas.PlaceCreate, commit: bool = True) -> models.Place:
        db_entity = models.Place(
            **schema.dict(),
        )

        self.db.add(db_entity)
        if commit:
            self.db.commit()
        else:
            self.db.flush()

        self.db.refresh(db_entity)

        return db_entity

    def get_by_id(self, id: int) -> models.Place:
        return self.db.query(models.Place).filter(models.Place.id == id).first()

    def suggest(self, to_find: str, amount: int) -> list[models.Place]:
        query = (self.db.query(models.Place)
                 .add_columns(func.levenshtein(models.Place.address, to_find).label('distance'))
                 .filter(models.Place.address.like(f'%{to_find}%'))
                 .order_by('distance')
                 .order_by(models.Place.population.desc())
                 .limit(amount)).all()
        print(query)
        res = []
        for q in query:
            res1 = q[0].__dict__
            res1["distance"] = q[1]
            res.append(res1)

        return res
