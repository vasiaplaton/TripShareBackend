from sqlalchemy import DateTime, ForeignKey, Boolean, Column, Integer, String, Enum

from app.database import Base
from app.entities.trip.models import Trip


class Stop(Base):
    __tablename__ = "stops"

    id = Column(Integer, primary_key=True)

    place = Column(String, nullable=False)
    place_name = Column(String, nullable=False)
    datetime = Column(DateTime, nullable=False)

    is_start = Column(Boolean, nullable=False)
    is_stop = Column(Boolean, nullable=False)
    num = Column(Integer, nullable=False)

    trip_id = Column(Integer, ForeignKey(Trip.__pk__, ondelete='CASCADE'), nullable=False)
