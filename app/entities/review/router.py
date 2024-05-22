from fastapi import HTTPException
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.entities.review import schemas
from app.entities.review.crud import ReviewCRUD
from app.entities.user.controller import User

review_router = APIRouter(
    prefix="/reviews",
    tags=["reviews"]
)


@review_router.post("/", response_model=schemas.ReviewReturn)
def create_review(review: schemas.ReviewGot, current_user: Annotated[User, Depends(User.get_current_user)], db: Session = Depends(get_db)):
    review_crud = ReviewCRUD(db)
    new_review = review_crud.create(schemas.ReviewCreate(**review.dict(), writer_id=current_user.schema.id))
    return new_review


@review_router.get("/{review_id}", response_model=schemas.ReviewReturn)
def get_review(review_id: int, db: Session = Depends(get_db)):
    review_crud = ReviewCRUD(db)
    review = review_crud.get_by_id(review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review


@review_router.delete("/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db)):
    review_crud = ReviewCRUD(db)
    review_crud.remove(review_id)
    return {"detail": "Review deleted successfully"}
