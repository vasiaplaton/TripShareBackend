from pydantic import BaseModel
import datetime

from app.entities.enums import TripStatus


class Stop(BaseModel):
    place: str
    place_name: str
    datetime: datetime.datetime

    num: int


class StopReturn(Stop):
    id: int
    is_start: bool
    is_stop: bool
    trip_id: int


class TripBase(BaseModel):
    max_passengers: int
    cost_sum: int

    max_two_passengers_in_the_back_seat: bool
    smoking_allowed: bool
    pets_allowed: bool
    free_trunk: bool


class TripCreate(TripBase):
    car_id: int
    stops: list[Stop]


class TripReturn(TripCreate):
    id: int
    driver_id: int

    status: TripStatus
    stops: list[StopReturn]
