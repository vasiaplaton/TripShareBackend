from typing import Optional

from pydantic import BaseModel


class Car(BaseModel):
    brand: str
    model: str
    color: str
    year_of_manufacture: int

    iamges_url: Optional[str] = None


class CarCreate(Car):
    user_id: int


class CarUpdate(Car):
    pass


class CarReturn(CarCreate):
    id: int
