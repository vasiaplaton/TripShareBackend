from typing import Optional

from pydantic import BaseModel


class CarGot(BaseModel):
    brand: str
    model: str
    color: str
    year_of_manufacture: int


class CarCreate(CarGot):
    user_id: int

    image0: str
    image1: Optional[str] = None
    image2: Optional[str] = None
    image3: Optional[str] = None


class CarReturn(CarGot):
    id: int

    image0_id: int
    image1_id: Optional[int] = None
    image2_id: Optional[int] = None
    image3_id: Optional[int] = None
