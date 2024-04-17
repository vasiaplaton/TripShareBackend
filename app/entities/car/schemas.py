from pydantic import BaseModel


class CarGot(BaseModel):
    brand: str
    model: str
    color: str
    year_of_manufacture: int
    photo: str


class CarCreate(CarGot):
    user_id: int


class CarReturn(BaseModel):
    id: int
