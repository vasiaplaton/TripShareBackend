from . import schemas, models
from ..request.models import Request
from ..stop.controller import Stop
from ..stop.schemas import StopCreate
from ...controllers.exceptions import NotFound, ValidateError
from ...database import SessionLocal
from ..enums import TripStatus, RequestStatus


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
        cls.db = SessionLocal()
        print(schema.car_id)
        # TODO checks??
        db_trip = models.Trip(
            **schema.dict(exclude={"stops"}),
            status=TripStatus.NEW,
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
    def found_for_user(cls, user_id: int):
        cls.db = SessionLocal()
        trips = cls.db.query(cls.model).filter(cls.model.driver_id == user_id).all()
        stops_got = [cls(trip) for trip in trips]
        return stops_got

    @classmethod
    def find_trips(cls, place_start: str, place_end: str):
        cls.db = SessionLocal()
        trips = cls.db.query(cls.model).all()
        return trips

    @classmethod
    def get_requests_by_trip_id(cls, trip_id: int, status: str = None) -> list[Request]:
        cls.db = SessionLocal()
        query = cls.db.query(Request).filter(Request.trip_id == trip_id)
        if status:
            query = query.filter(Request.status == status)
        return query.all()

    def update_trip(self):
        # Получаем все запросы для данной поездки со статусом "ACCEPTED" или "CREATED"
        requests = self.get_requests_by_trip_id(self.db.trip_id, status=RequestStatus.ACCEPTED.value)
        # Подсчитываем количество занятых мест
        occupied_seats = sum(req.number_of_seats for req in requests)
        # Подсчитываем количество свободных мест
        available_seats = self.db_entity.max_passengers - occupied_seats
        self.db_entity.available_seats = available_seats

        if len(requests) != 0:
            if self.db_entity.status == TripStatus.NEW.value:
                self.db_entity.status = TripStatus.BRONED.value
        self.db.commit()
        self.db.refresh(self.db_entity)

        if available_seats == 0:
            self.db_entity.status = TripStatus.FULLY_BRONNED.value
            # Отклоняем все остальные запросы
            for req in requests:
                if req.status == RequestStatus.CREATED:
                    req.status = RequestStatus.DECLINED.value
            self.db.commit()

        self.db.commit()
        self.db.refresh(self.db_entity)


