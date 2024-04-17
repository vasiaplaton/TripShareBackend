from app.database import Base

from sqlalchemy import DateTime, ForeignKey, Boolean, Column, Integer, String, Enum

from ..car.models import Car
from ..user.models import User
from app.database import Base
from ..enums import TripStatus


class Trip(Base):
    __tablename__ = "trips"
    __pk__ = "trips.id"

    id = Column(Integer, primary_key=True)

    max_passengers = Column(Integer, nullable=False)

    cost_sum = Column(Integer, nullable=False)

    max_two_passengers_in_the_back_seat = Column(Boolean, nullable=False)
    smoking_allowed = Column(Boolean, nullable=False)
    e_cigarettes_allowed = Column(Boolean, nullable=False)
    pets_allowed = Column(Boolean, nullable=False)
    free_trunk = Column(Boolean, nullable=False)
    status = Column(Enum(TripStatus), nullable=False)

    car_id = Column(Integer, ForeignKey(Car.__pk__, ondelete='CASCADE'), nullable=False)
    driver_id = Column(Integer, ForeignKey(User.__pk__, ondelete='CASCADE'), nullable=False)
