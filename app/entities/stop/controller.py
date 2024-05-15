from . import schemas, models
from ...controllers.exceptions import NotFound
from ...database import SessionLocal


class Stop:
    model = models.Stop

    def __init__(self, id_got: int, db: SessionLocal):
        stop = db.query(self.model).filter(self.model.id == id_got).first()
        if not stop:
            raise NotFound()

        self.db_entity: models.Stop = stop

    @classmethod
    def create(cls, schema: schemas.StopCreate, db: SessionLocal):
        db_stop = cls.model(
            **schema.dict()
        )

        db.add(db_stop)
        db.commit()
        db.refresh(db_stop)
        return cls(db_stop.id, db)

    @classmethod
    def get_for_trip(cls, trip_id: int, db: SessionLocal) -> list['Stop']:
        stops = db.query(cls.model).filter(cls.model.trip_id == trip_id).all()
        stops_got = [cls(stop.id, db) for stop in stops]
        return stops_got

    @property
    def schema(self) -> schemas.StopReturn:
        return schemas.StopReturn(**self.db_entity.__dict__, avatar=None)

    def calculate_dist(self, another_place: str) -> float:
        # TODO
        pass
