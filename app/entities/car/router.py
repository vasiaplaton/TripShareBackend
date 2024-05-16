from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from . import schemas
from . import controller
from ..user.controller import User
from ...dependencies import get_db

car_router = APIRouter(
    prefix="/cars",
    tags=["cars"]
)


@car_router.post("/")
async def create_car(schema: schemas.CarGot,
                     current_user: Annotated[User, Depends(User.get_current_user)],
                     db: Session = Depends(get_db)) -> schemas.CarReturn:
    """Добавляем машину пользователю"""
    return controller.Car.create(schemas.CarCreate(**schema.dict(), user_id=current_user.schema.id), db).schema


@car_router.get("/me")
async def get_my_cars(current_user: Annotated[User, Depends(User.get_current_user)],
                      db: Session = Depends(get_db)) -> list[schemas.CarReturn]:
    """Получаем текущего машины пользователя"""
    return controller.Car.found_for_user(current_user.schema.id, db)


@car_router.get("/user/{user_id}")
async def get_for_user(user_id: int, db: Session = Depends(get_db)):
    """Получаем машины пользователя"""
    return controller.Car.found_for_user(user_id, db)