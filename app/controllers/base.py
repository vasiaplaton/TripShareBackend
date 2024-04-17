from app import models
from app.database import SessionLocal


class ABSModel:
    model = models.User
    db = SessionLocal()

