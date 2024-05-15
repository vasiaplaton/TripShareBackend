from app.database import Base

from sqlalchemy import DateTime, ForeignKey, Boolean, Column, Integer, String, Enum

from app.database import Base


class Image(Base):
    __tablename__ = "images"
    __pk__ = "images.id"

    id = Column(Integer, primary_key=True)

    filename = Column(String, nullable=False)
