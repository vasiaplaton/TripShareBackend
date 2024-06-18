import datetime

from pydantic import BaseModel

from app.entities.enums import RequestStatus


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
