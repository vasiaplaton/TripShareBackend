from sqlalchemy import ForeignKey, Column, Integer, String

from app.database import Base
from app.entities.images.models import Image


class Car(Base):
    __tablename__ = "cars"
    __pk__ = "cars.id"

    id = Column(Integer, primary_key=True)

    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    color = Column(String, nullable=False)
    year_of_manufacture = Column(Integer, nullable=False)

    image0_id = Column(Integer, ForeignKey(Image.__pk__, ondelete='CASCADE'), nullable=True)
    image1_id = Column(Integer, ForeignKey(Image.__pk__, ondelete='CASCADE'), nullable=True)
    image2_id = Column(Integer, ForeignKey(Image.__pk__, ondelete='CASCADE'), nullable=True)
    image3_id = Column(Integer, ForeignKey(Image.__pk__, ondelete='CASCADE'), nullable=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)