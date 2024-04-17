import datetime
from pydantic import BaseModel


class StopInTrip(BaseModel):
    place: str
    place_name: str
    datetime: datetime.datetime

    num: int


class StopCreate(StopInTrip):
    is_start: bool
    is_stop: bool
    trip_id: int


class StopReturn(StopCreate):
    id: int
