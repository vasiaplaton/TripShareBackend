from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.entities.car import schemas
from app.entities.car.crud import CarCrud, _model_to_schema, _models_to_schema
from app.entities.user.crud import get_current_user
from app.entities.user.schemas import UserReturn

car_router = APIRouter(
    prefix="/cars",
    tags=["cars"]
)


@car_router.post("/", response_model=schemas.CarReturn)
async def create_car(schema: schemas.Car,
                     current_user: Annotated[UserReturn, Depends(get_current_user)],
                     db: Session = Depends(get_db)) -> schemas.CarReturn:
    """Добавляем машину пользователю"""
    return _model_to_schema(CarCrud(db).create(schemas.CarCreate(**schema.dict(), user_id=current_user.id)))


@car_router.get("/me", response_model=list[schemas.CarReturn])
async def get_my_cars(current_user: Annotated[UserReturn, Depends(get_current_user)],
                      db: Session = Depends(get_db)) -> list[schemas.CarReturn]:
    """Получаем текущего машины пользователя"""
    return _models_to_schema(CarCrud(db).get_by_user_id(current_user.id))


@car_router.get("/user/{user_id}", response_model=list[schemas.CarReturn])
async def get_for_user(user_id: int, db: Session = Depends(get_db)):
    """Получаем машины пользователя"""
    return _models_to_schema(CarCrud(db).get_by_user_id(user_id))


@car_router.delete("/{id}", response_model=schemas.CarReturn)
async def delete_my_car(id: int,
                      current_user: Annotated[UserReturn, Depends(get_current_user)],
                      db: Session = Depends(get_db)) -> schemas.CarReturn:
    car = CarCrud(db).get_by_id(id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    if car.user_id != current_user.id:
        raise HTTPException(status_code=401, detail="Car not found")

    return _model_to_schema(car)