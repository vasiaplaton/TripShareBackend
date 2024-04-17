from pydantic import BaseModel
from ..enums import TripStatus
from ..stop.schemas import StopInTrip, StopReturn


class Trip(BaseModel):
    max_passengers: int
    cost_sum: int
    max_two_passengers_in_the_back_seat: bool
    smoking_allowed: bool
    e_cigarettes_allowed: bool
    pets_allowed: bool
    free_trunk: bool


class TripGot(Trip):
    car_id: int
    stops: list[StopInTrip]


class TripCreate(TripGot):
    driver_id: int


class TripReturn(BaseModel):
    id: int

    status: TripStatus
    stops: list[StopReturn]
