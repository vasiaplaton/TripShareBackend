from typing import Optional

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    # TODO validate phone
    phone: str
    name: str
    talkativeness: Optional[int] = Field(None, ge=0, le=10)
    attitude_towards_smoking: Optional[int] = Field(None, ge=0, le=10)
    attitude_towards_animals_during_the_trip: Optional[int] = Field(None, ge=0, le=10)


class UserCreate(UserBase):
    password: str
    avatar: Optional[str] = None


class UserReturn(UserBase):
    id: int
    rating: Optional[float] = None
    avatar_id: Optional[int] = None


class UserUpdate(UserBase):
    avatar: Optional[str] = None
