from typing import Optional

from pydantic import BaseModel


class ReviewCreate(BaseModel):
    text: str
    rating: int
    image_url: Optional[str] = None
    user_id: int


class ReviewReturn(ReviewCreate):
    id: int
    writer_id: int
