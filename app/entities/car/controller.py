from . import schemas, models
from ...controllers.exceptions import NotFound
from ...database import SessionLocal


class Car:
    model = models.Car
    db = SessionLocal()

    def __init__(self, id_got: int):
        car = self.db.query(self.model).filter(self.model.id == id_got).first()
        if not car:
            raise NotFound()

        self.db_entity: models.Car = car

    @classmethod
    def create(cls, schema: schemas.CarCreate):
        # TODO validate
        db_car = cls.model(
            **schema.dict()
        )

        cls.db.add(db_car)
        cls.db.commit()
        cls.db.refresh(db_car)
        return cls(db_car.id)

    def _update(self):
        self.db.refresh(self.db_entity)

    @property
    def schema(self) -> schemas.CarReturn:
        self._update()

        return schemas.CarReturn(**self.db_entity.__dict__)

    @classmethod
    def found_for_user(cls, user_id: int) -> list[schemas.CarReturn]:
        cars = cls.db.query(cls.model).filter(cls.model.user_id == user_id).all()
        cars_got = [cls(trip).schema for trip in cars]
        return cars_got
