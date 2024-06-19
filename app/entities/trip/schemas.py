from typing import Optional

from pydantic import BaseModel
import datetime

from app.entities.enums import TripStatus
from app.entities.trip.comfrots_schemas import ComfortsInTrip


class Place(BaseModel):
    place: str
    place_name: str


class Stop(Place):
    datetime: datetime.datetime

    num: int


class StopReturn(Stop):
    id: int
    is_start: bool
    is_stop: bool
    trip_id: int


class TripBase(ComfortsInTrip):
    max_passengers: int
    cost_sum: int


class TripCreate(TripBase):
    car_id: int
    stops: list[Stop]


class TripReturn(TripCreate):
    id: int
    driver_id: int

    status: TripStatus
    stops: Optional[list[StopReturn]] = None
