from typing import Annotated

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.entities.trip import schemas, crud
from app.entities.trip.crud import TripCrud
from app.entities.user.crud import get_current_user
from app.entities.user.schemas import UserReturn

trip_router = APIRouter(
    prefix="/trips",
    tags=["trips"]
)


@trip_router.post("/")
async def create_trip(schema: schemas.TripCreate,
                      current_user: Annotated[UserReturn, Depends(get_current_user)],
                      db: Session = Depends(get_db) ) -> schemas.TripReturn:
    """Создаем поездку"""
    return crud._model_to_schema(TripCrud(db).create(schema, current_user.id), db)


@trip_router.get("/me_as_driver")
async def get_as_writer(current_user: Annotated[UserReturn, Depends(get_current_user)],
                       db: Session = Depends(get_db)):
    return crud._models_to_schema(TripCrud(db).get_by_driver_id(current_user.id), db)


@trip_router.get("/get_all")
async def get_all(db: Session = Depends(get_db)):
    return crud._models_to_schema(TripCrud(db).get_all(), db)



@trip_router.get("/{id}}")
async def get_all(id: int, db: Session = Depends(get_db)) -> schemas.TripReturn:
    return crud._model_to_schema(TripCrud(db).get_by_id(id), db)
