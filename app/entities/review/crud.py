from typing import Optional

from fastapi import HTTPException

from app.database import SessionLocal
from app.entities.review import models, schemas


class ReviewCRUD:
    def __init__(self, db: SessionLocal):
        self.db = db

    def get_by_id(self, r_id: int) -> Optional[models.Review]:
        trip = self.db.query(models.Review).filter(models.Review.id == r_id).first()
        return trip

    def remove(self, r_id: int):
        review = self.get_by_id(r_id)
        if review is None:
            raise HTTPException(status_code=404, detail="Not found")

    def create(self, schema: schemas.ReviewCreate) -> Optional[models.Review]:
        model = models.Review(**schema.dict())

        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return model

    def get_reviews_by_user_id(self, user_id: int) -> list[models.Review]:
        reviews = self.db.query(models.Review).filter(models.Review.user_id == user_id).all()
        return reviews
