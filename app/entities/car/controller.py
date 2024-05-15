from . import schemas, models
from ...controllers.exceptions import NotFound
from ...database import SessionLocal


class Car:
    model = models.Car

    def __init__(self, id_got: int, db: SessionLocal):
        car = db.query(self.model).filter(self.model.id == id_got).first()
        if not car:
            raise NotFound()

        self.db_entity: models.Car = car

    @classmethod
    def create(cls, schema: schemas.CarCreate, db: SessionLocal):
        # TODO validate
        db_car = cls.model(
            **schema.dict()
        )

        db.add(db_car)
        db.commit()
        db.refresh(db_car)
        return cls(db_car.id, db)

    @property
    def schema(self) -> schemas.CarReturn:
        return schemas.CarReturn(**self.db_entity.__dict__)

    @classmethod
    def found_for_user(cls, user_id: int, db: SessionLocal) -> list[schemas.CarReturn]:
        cars = db.query(cls.model).filter(cls.model.user_id == user_id).all()
        cars_got = [cls(car.id, db).schema for car in cars]
        return cars_got
