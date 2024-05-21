from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from . import schemas
from .crud import CarCRUD
from ..user.controller import User
from ...dependencies import get_db

car_router = APIRouter(
    prefix="/cars",
    tags=["cars"]
)


@car_router.post("/", response_model=schemas.CarCreate)
async def create_car(schema: schemas.CarGot,
                     current_user: Annotated[User, Depends(User.get_current_user)],
                     db: Session = Depends(get_db)) -> schemas.CarReturn:
    """Добавляем машину пользователю"""
    return CarCRUD(db).create_car(schemas.CarCreate(**schema.dict(), user_id=current_user.schema.id))


@car_router.get("/me", response_model=list[schemas.CarCreate])
async def get_my_cars(current_user: Annotated[User, Depends(User.get_current_user)],
                      db: Session = Depends(get_db)) -> list[schemas.CarReturn]:
    """Получаем текущего машины пользователя"""
    return CarCRUD(db).get_car_by_id(current_user.schema.id)


@car_router.get("/user/{user_id}", response_model=list[schemas.CarCreate])
async def get_for_user(user_id: int, db: Session = Depends(get_db)):
    """Получаем машины пользователя"""
    return CarCRUD(db).get_car_by_id(user_id)
