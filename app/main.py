from fastapi import FastAPI

from app.entities.car.router import car_router
from app.entities.trip.router import trip_router
from app.entities.user.router import user_router

app = FastAPI()


app.include_router(user_router)
app.include_router(trip_router)
app.include_router(car_router)
