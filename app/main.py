from fastapi import FastAPI

from app.entities.car.router import car_router
from app.entities.chats.router import chat_router
from app.entities.pays.router import pays_router
from app.entities.places.router import places_router
from app.entities.requests.router import request_router
from app.entities.review.router import review_router
from app.entities.trip.router import trip_router
from app.entities.user.router import user_router
from app.suggest.router import yandex_router

app = FastAPI()


app.include_router(user_router)
app.include_router(car_router)
app.include_router(chat_router)
app.include_router(review_router)
app.include_router(trip_router)
app.include_router(request_router)
# app.include_router(yandex_router)
app.include_router(places_router)
app.include_router(pays_router)