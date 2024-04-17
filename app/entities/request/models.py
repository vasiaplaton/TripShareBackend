from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Enum

from app.database import Base
from app.entities.enums import RequestStatus


class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True)

    request_datetime = Column(DateTime, nullable=False)
    status = Column(Enum(RequestStatus), nullable=False)
    status_change_datetime = Column(DateTime, nullable=True)
    cost = Column(Integer, nullable=False)
    number_of_seats = Column(Integer, nullable=False)

    departure_id = Column(Integer, ForeignKey("stops.id", ondelete='CASCADE'), nullable=False)
    arrival_id = Column(Integer, ForeignKey("stops.id", ondelete='CASCADE'), nullable=False)

    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
    trip_id = Column(Integer, ForeignKey("trips.id", ondelete='CASCADE'), nullable=False)