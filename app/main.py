from fastapi import FastAPI

from app.entities.car.router import car_router
from app.entities.chat.router import chat_router
from app.entities.images.router import image_router
from app.entities.request.router import request_router
from app.entities.review.router import review_router
from app.entities.trip.router import trip_router
from app.entities.user.router import user_router

app = FastAPI()


app.include_router(user_router)
app.include_router(trip_router)
app.include_router(car_router)
app.include_router(image_router)
app.include_router(chat_router)
app.include_router(request_router)
app.include_router(review_router)