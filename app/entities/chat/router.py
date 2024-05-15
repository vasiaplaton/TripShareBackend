from typing import Annotated

from fastapi import APIRouter, Depends

from . import schemas
from . import controller
from ..user.controller import User

car_router = APIRouter(
    prefix="/cars",
    tags=["cars"]
)


@car_router.post("/")
async def create_car(schema: schemas.CarGot,
                     current_user: Annotated[User, Depends(User.get_current_user)]) -> schemas.CarReturn:
    """Добавляем машину пользователю"""
    return controller.Car.create(schemas.CarCreate(**schema.dict(), user_id=current_user.schema.id)).schema


@car_router.get("/me")
async def get_my_cars(current_user: Annotated[User, Depends(User.get_current_user)]) -> list[schemas.CarReturn]:
    """Получаем текущего машины пользователя"""
    return controller.Car.found_for_user(current_user.schema.id)


@car_router.get("/user/{user_id}")
async def create_car(user_id: int):
    """Получаем машины пользователя"""
    return controller.Car.found_for_user(user_id)