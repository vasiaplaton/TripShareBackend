from sqlalchemy import ForeignKey, Column, Integer, String

from app.database import Base


class Car(Base):
    __tablename__ = "cars"
    __pk__ = "cars.id"

    id = Column(Integer, primary_key=True)

    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    color = Column(String, nullable=False)
    year_of_manufacture = Column(Integer, nullable=False)
    photo = Column(String, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)