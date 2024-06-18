from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.entities.review import schemas
from app.entities.review.crud import _model_to_schema, ReviewCrud, _models_to_schema
from app.entities.user.crud import get_current_user
from app.entities.user.schemas import UserReturn

review_router = APIRouter(
    prefix="/reviews",
    tags=["reviews"]
)


@review_router.post("/", response_model=schemas.ReviewReturn)
async def create_car(schema: schemas.ReviewCreate,
                     current_user: Annotated[UserReturn, Depends(get_current_user)],
                     db: Session = Depends(get_db)) -> schemas.ReviewReturn:
    return _model_to_schema(ReviewCrud(db).create(schema, writer_id=current_user.id))


@review_router.get("/user/{user_id}", response_model=list[schemas.ReviewReturn])
async def get_for_user(user_id: int, db: Session = Depends(get_db)):
    return _models_to_schema(ReviewCrud(db).get_by_user_id(user_id))


@review_router.get("/me", response_model=list[schemas.ReviewReturn])
async def get_for_user(current_user: Annotated[UserReturn, Depends(get_current_user)],
                       db: Session = Depends(get_db)):
    return _models_to_schema(ReviewCrud(db).get_by_user_id(current_user.id))


@review_router.get("/me_as_writer", response_model=list[schemas.ReviewReturn])
async def get_as_writer(current_user: Annotated[UserReturn, Depends(get_current_user)],
                       db: Session = Depends(get_db)):
    return _models_to_schema(ReviewCrud(db).get_by_writer_id(current_user.id))



