from pydantic import BaseModel


class ReviewGot(BaseModel):
    text: str
    rating: int
    image_id: int
    user_id: int


class ReviewCreate(ReviewGot):
    writer_id: int


class ReviewReturn(ReviewCreate):
    id: int
