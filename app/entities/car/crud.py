from app.controllers.exceptions import NotFound
from app.database import SessionLocal
from app.entities.car import models, schemas


class CarCRUD:
    def __init__(self, db: SessionLocal):
        self.db = db

    def get_car_by_id(self, id_got: int) -> models.Car:
        car = self.db.query(models.Car).filter(models.Car.id == id_got).first()
        if not car:
            raise NotFound()
        return car

    def create_car(self, schema: schemas.CarCreate) -> models.Car:
        # TODO validate
        db_car = models.Car(**schema.dict())
        self.db.add(db_car)
        self.db.commit()
        self.db.refresh(db_car)
        return db_car

    def get_cars_by_user_id(self, user_id: int) -> list[models.Car]:
        cars = self.db.query(models.Car).filter(models.Car.user_id == user_id).all()
        return cars