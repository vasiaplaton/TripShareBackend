from datetime import datetime

from pydantic import BaseModel

from app.entities.enums import RequestStatus


class Request(BaseModel):
    cost: str
    number_of_seats: str
    departure_id: str
    arrival_id: str
    trip_id: str


class RequestGot(Request):
    pass


class RequestReturn(Request):
    id: int
    request_datetime: datetime
    status: RequestStatus
    status_change_datetime: datetime


"""
request_datetime = Column(DateTime, nullable=False)
    status = Column(Enum(RequestStatus), nullable=False)
    status_change_datetime = Column(DateTime, nullable=True)
    cost = Column(Integer, nullable=False)
    number_of_seats = Column(Integer, nullable=False)

    departure_id = Column(Integer, ForeignKey("stops.id", ondelete='CASCADE'), nullable=False)
    arrival_id = Column(Integer, ForeignKey("stops.id", ondelete='CASCADE'), nullable=False)

    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
    trip_id = Column(Integer, ForeignKey("trips.id", ondelete='CASCADE'), nullable=False)"""
