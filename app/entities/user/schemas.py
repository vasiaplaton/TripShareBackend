from typing import Optional

from pydantic import BaseModel, Field

from app.entities.car.schemas import CarReturn


class UserBase(BaseModel):
    # TODO validate phone
    phone: str
    name: str

    surname: str
    email: Optional[str] = None
    birthday: str
    musicPreferences: Optional[str] = None
    info: Optional[str] = None

    talkativeness: Optional[int] = Field(None, ge=0, le=10)
    attitude_towards_smoking: Optional[int] = Field(None, ge=0, le=10)
    attitude_towards_animals_during_the_trip: Optional[int] = Field(None, ge=0, le=10)


class UserCreate(UserBase):
    password: str
    avatar_url: Optional[str] = None


class UserReturn(UserBase):
    id: int
    rating: Optional[float] = None
    avatar_url: Optional[str] = None
    cars: Optional[list[CarReturn]] = None


class UserUpdate(UserBase):
    avatar: Optional[str] = None
