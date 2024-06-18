from typing import Optional

from app.database import models
from app.entities.user import crud as user_crud
from app.database.database import SessionLocal
from app.entities.review import schemas
from app.entities.exceptions import NotFound
from app.entities.user.crud import UserCrud


def _model_to_schema(db_item: models.Review, db: SessionLocal, user_dto: bool = True) -> Optional[schemas.ReviewReturn]:
    if db_item is None:
        return None
    d = db_item.__dict__
    if user_dto:
        d["user"] = user_crud._model_to_schema(UserCrud(db).get_user_by_id(db_item.user_id), db, car_dto=False)
        d["writer"] = user_crud._model_to_schema(UserCrud(db).get_user_by_id(db_item.writer_id), db, car_dto=False)
    return schemas.ReviewReturn.model_validate(db_item.__dict__)


def _models_to_schema(db_items: list[models.Car], db: SessionLocal, user_dto: bool = True) -> list[schemas.ReviewReturn]:
    return [_model_to_schema(db_item, db, user_dto) for db_item in db_items]


class ReviewCrud:
    def __init__(self, db: SessionLocal):
        self.db = db

    def create(self, schema: schemas.ReviewCreate, writer_id: int, commit: bool = True) -> models.Review:
        db_entity = models.Review(
            **schema.dict(),
            writer_id=writer_id
        )

        self.db.add(db_entity)
        if commit:
            self.db.commit()
        else:
            self.db.flush()

        self.db.refresh(db_entity)

        reviews = self.get_by_user_id(db_entity.user_id)
        summm = 0
        for i in reviews:
            summm += i.rating

        UserCrud(self.db).update_rating(db_entity.user_id, summm / len(reviews), commit=True)
        self.db.refresh(db_entity)
        return db_entity

    def get_by_id(self, id: int) -> list[models.Review]:
        return self.db.query(models.Review).filter(models.Review.id == id).all()

    def get_by_user_id(self, user_id: int) -> list[models.Review]:
        return self.db.query(models.Review).filter(models.Review.user_id == user_id).all()

    def get_by_writer_id(self, writer_id: int) -> list[models.Review]:
        return self.db.query(models.Review).filter(models.Review.writer_id == writer_id).all()

    def delete(self, id: int, commit: bool = True):
        res = self.db.query(models.Review).filter(
            models.Review.id == id).first()
        if res is None:
            raise NotFound
        res.delete()
        if commit:
            self.db.commit()
        else:
            self.db.flush()
