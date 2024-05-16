from . import schemas, models
from ..request.models import Request
from ..stop.controller import Stop
from ..stop.schemas import StopCreate
from ...controllers.exceptions import NotFound, ValidateError
from ...database import SessionLocal
from ..enums import TripStatus, RequestStatus


class Trip:
    model = models.Trip

    def __init__(self, id_got: int, db: SessionLocal):
        trip = db.query(self.model).filter(self.model.id == id_got).first()
        if not trip:
            raise NotFound()

        self.db_entity: models.Trip = trip

    @classmethod
    def create(cls, schema: schemas.TripCreate, db: SessionLocal) -> 'Trip':
        print(schema.car_id)
        # TODO checks??
        db_trip = models.Trip(
            **schema.dict(exclude={"stops"}),
            status=TripStatus.NEW,
        )

        db.add(db_trip)
        db.commit()
        db.refresh(db_trip)

        stops = schema.stops
        if len(stops) < 2:
            raise ValidateError()

        stops.sort(key=lambda stop: stop.num)

        stops = [StopCreate(**stop.dict(), trip_id=db_trip.id, is_start=False, is_stop=False) for stop in stops]

        stops[0].is_start = True
        stops[-1].is_stop = True
        for stop in stops:
            Stop.create(stop, db)

        return cls(db_trip.id, db)

    def schema(self, db: SessionLocal) -> schemas.TripReturn:
        stops = Stop.get_for_trip(self.db_entity.id, db)
        stops = [stop.schema for stop in stops]

        return schemas.TripReturn(**self.db_entity.__dict__, stops=stops)

    @classmethod
    def found_for_user(cls, user_id: int, db: SessionLocal):
        trips = db.query(cls.model).filter(cls.model.driver_id == user_id).all()
        stops_got = [cls(trip, db) for trip in trips]
        return stops_got

    @classmethod
    def find_trips(cls, place_start: str, place_end: str, db: SessionLocal):
        trips = db.query(cls.model).all()
        return trips

    @classmethod
    def get_requests_by_trip_id(cls, trip_id: int , db: SessionLocal, status: str = None) -> list[Request]:
        query = db.query(Request).filter(Request.trip_id == trip_id)
        if status:
            query = query.filter(Request.status == status)
        return query.all()

    def recount_available_seats(self, db: SessionLocal):
        # Получаем все запросы для данной поездки со статусом "ACCEPTED" или "CREATED"
        requests = self.get_requests_by_trip_id(db.trip_id, db, status=RequestStatus.ACCEPTED.value)
        # Подсчитываем количество занятых мест
        occupied_seats = sum(req.number_of_seats for req in requests)
        # Подсчитываем количество свободных мест
        available_seats = self.db_entity.max_passengers - occupied_seats
        self.db_entity.available_seats = available_seats

        db.commit()

    def update_trip(self, db: SessionLocal):
        # Получаем все запросы для данной поездки со статусом "ACCEPTED" или "CREATED"
        requests = self.get_requests_by_trip_id(db.trip_id, db, status=RequestStatus.ACCEPTED.value)
        self.recount_available_seats(db)

        if len(requests) != 0:
            if self.db_entity.status == TripStatus.NEW.value:
                self.db_entity.status = TripStatus.BRONED.value
        db.commit()
        db.refresh(self.db_entity)

        if available_seats == 0:
            self.db_entity.status = TripStatus.FULLY_BRONNED.value
            # Отклоняем все остальные запросы
            for req in requests:
                if req.status == RequestStatus.CREATED:
                    req.status = RequestStatus.DECLINED.value
            db.commit()

        db.commit()
        db.refresh(self.db_entity)
