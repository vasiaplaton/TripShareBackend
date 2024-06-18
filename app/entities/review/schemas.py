from typing import Optional

from pydantic import BaseModel

from app.entities.user.schemas import UserReturn


class ReviewCreate(BaseModel):
    text: str
    rating: int
    image_url: Optional[str] = None
    user_id: int


class ReviewReturn(ReviewCreate):
    id: int
    writer_id: int

    user: Optional[UserReturn] = None
    writer: Optional[UserReturn] = None
