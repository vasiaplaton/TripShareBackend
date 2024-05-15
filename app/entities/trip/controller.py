from . import schemas, models
from ..stop.controller import Stop
from ..stop.schemas import StopCreate
from ...controllers.exceptions import NotFound, ValidateError
from ...database import SessionLocal
from ..enums import TripStatus


class Trip:
    model = models.Trip
    db = SessionLocal()

    def __init__(self, id_got: int):
        trip = self.db.query(self.model).filter(self.model.id == id_got).first()
        if not trip:
            raise NotFound()

        self.db_entity: models.Trip = trip

    @classmethod
    def create(cls, schema: schemas.TripCreate) -> 'Trip':
        # TODO checks??
        db_trip = cls.model(
            **schema.dict(exclude={"stops"}),
            status=TripStatus.NEW
        )

        cls.db.add(db_trip)
        cls.db.commit()
        cls.db.refresh(db_trip)

        stops = schema.stops
        if len(stops) < 2:
            raise ValidateError()

        stops.sort(key=lambda stop: stop.num)

        stops = [StopCreate(**stop.dict(), trip_id=db_trip.id, is_start=False, is_stop=False) for stop in stops]

        stops[0].is_start = True
        stops[-1].is_stop = True
        for stop in stops:
            Stop.create(stop)

        return cls(db_trip.id)

    def _update(self):
        self.db.refresh(self.db_entity)

    @property
    def schema(self) -> schemas.TripReturn:
        self._update()
        stops = Stop.get_for_trip(self.db_entity.id)
        stops = [stop.schema for stop in stops]

        return schemas.TripReturn(**self.db_entity.__dict__, stops=stops)

    @classmethod
    def find(cls, geo_start: str, geo_end: str):
        pass

    @classmethod
    def found_for_user(cls, user_id: int):
        trips = cls.db.query(cls.model).filter(cls.model.driver_id == user_id).all()
        stops_got = [cls(trip) for trip in trips]
        return stops_got


    @classmethod
    def find_trips(cls, place_start: str, place_end: str):
        trips = cls.db.query(cls.model).all()
        return trips

