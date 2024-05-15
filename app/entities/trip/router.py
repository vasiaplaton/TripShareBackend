from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from . import schemas
from . import controller
from ..user.controller import User

trip_router = APIRouter(
    prefix="/trips",
    tags=["trips"]
)


@trip_router.post("/")
async def create_trip(schema: schemas.TripGot,
                      current_user: Annotated[User, Depends(User.get_current_user)]) -> schemas.TripReturn:
    """Создаем поездку"""
    return controller.Trip.create(schemas.TripCreate(**schema.dict(), driver_id=current_user.schema.id)).schema


@trip_router.get("/as_driver")
async def get_trips(current_user: Annotated[User, Depends(User.get_current_user)]) -> list[schemas.TripReturn]:
    """Получаем наши поездки как водителя"""
    return controller.Trip.found_for_user(current_user.schema.id)


# TODO все поездки
@trip_router.get("/search", response_model=list[schemas.TripReturn])
async def search(place_start: str, place_end: str):
    return controller.Trip.find_trips(place_start, place_end)
