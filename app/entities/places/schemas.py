from pydantic import BaseModel


class PlaceCreate(BaseModel):
    region: str
    municipality: str
    settlement: str
    type: str
    address: str
    population: int
    latitude_dd: float
    longitude_dd: float


class PlaceReturn(PlaceCreate):
    id: int