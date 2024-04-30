from sqlalchemy import ForeignKey, Column, Integer, String

from app.database import Base
from app.entities.images.models import Image


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)

    text = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)

    image_id = Column(Integer, ForeignKey(Image.__pk__, ondelete='CASCADE'), nullable=False)
    writer_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)

