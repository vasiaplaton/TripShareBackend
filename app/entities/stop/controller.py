from . import schemas, models
from ...controllers.exceptions import NotFound
from ...database import SessionLocal


class Stop:
    model = models.Stop
    db = SessionLocal()

    def __init__(self, id_got: int):
        stop = self.db.query(self.model).filter(self.model.id == id_got).first()
        if not stop:
            raise NotFound()

        self.db_entity: models.Stop = stop

    @classmethod
    def create(cls, schema: schemas.StopCreate):
        db_stop = cls.model(
            **schema.dict()
        )

        cls.db.add(db_stop)
        cls.db.commit()
        cls.db.refresh(db_stop)
        return cls(db_stop.id)

    @classmethod
    def get_for_trip(cls, trip_id: int) -> list['Stop']:
        stops = cls.db.query(cls.model).filter(cls.model.trip_id == trip_id).all()
        stops_got = [cls(stop.id) for stop in stops]
        return stops_got

    def _update(self):
        self.db.refresh(self.db_entity)

    @property
    def schema(self) -> schemas.StopReturn:
        self._update()

        return schemas.StopReturn(**self.db_entity.__dict__, avatar=None)

    def calculate_dist(self, another_place: str) -> float:
        # TODO
        pass
