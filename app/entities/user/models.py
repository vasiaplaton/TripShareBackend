from sqlalchemy import Column, Integer, String, ForeignKey

from app.database import Base
from app.entities.images.models import Image


class User(Base):
    __tablename__ = "users"
    __pk__ = "users.id"

    id = Column(Integer, primary_key=True)

    phone = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)

    name = Column(String, nullable=False)

    surname = Column(String, nullable=False)
    email = Column(String, nullable=True)
    birthday = Column(String, nullable=False)
    musicPreferences = Column(String, nullable=True)
    info = Column(String, nullable=True)

    rating = Column(Integer, nullable=True)

    # favorite genres
    talkativeness = Column(Integer, nullable=True)
    attitude_towards_smoking = Column(Integer, nullable=True)
    attitude_towards_animals_during_the_trip = Column(Integer, nullable=True)

    avatar_id = Column(Integer, ForeignKey(Image.__pk__, ondelete='CASCADE'), nullable=True)
