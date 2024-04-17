from sqlalchemy import ForeignKey, Column, Integer, String

from app.database import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)

    text = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)

    writer_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)

