from typing import Optional

from pydantic import BaseModel


class CarGot(BaseModel):
    brand: str
    model: str
    color: str
    year_of_manufacture: int

    image0_id: int
    image1_id: Optional[int] = None
    image2_id: Optional[int] = None
    image3_id: Optional[int] = None


class CarCreate(CarGot):
    user_id: int


class CarReturn(CarCreate):
    id: int
