import datetime

from pydantic import BaseModel

from app.entities.enums import RequestStatus
from app.entities.trip.comfrots_schemas import ComfortsInTrip
from app.entities.trip.schemas import StopReturn, TripReturn, Place
from app.entities.user.schemas import UserReturn


class Request(BaseModel):
    number_of_seats: int
    departure_id: int
    arrival_id: int
    trip_id: int


class RequestReturn(Request):
    cost: int
    user_id: int
    id: int
    request_datetime: datetime.datetime
    status: RequestStatus
    status_change_datetime: datetime.datetime


class RequestReturnUser(RequestReturn):
    user: UserReturn


class RequestReturnWithTrip(RequestReturn):
    trip: TripReturn


class FindRequest(BaseModel):
    start: Place
    end: Place
    comforts: ComfortsInTrip
    date: datetime.datetime
    needed_seats: int


class FindResult(BaseModel):
    start_distance: int
    start: StopReturn
    end_distance: int
    end: StopReturn
    trip: TripReturn
    cost: int
