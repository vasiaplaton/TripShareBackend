from sqlalchemy import Column, Integer, String

from app.database import Base


class User(Base):
    __tablename__ = "users"
    __pk__ = "users.id"

    id = Column(Integer, primary_key=True)

    phone = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)

    name = Column(String, nullable=False)
    rating = Column(Integer, nullable=True)

    # favorite genres
    talkativeness = Column(Integer, nullable=True)
    attitude_towards_smoking = Column(Integer, nullable=True)
    attitude_towards_animals_during_the_trip = Column(Integer, nullable=True)

    avatar_path = Column(String, nullable=True)
