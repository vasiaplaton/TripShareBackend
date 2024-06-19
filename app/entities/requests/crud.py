import datetime
from typing import Optional

from sqlalchemy import or_

from app.database import models
from app.database.database import SessionLocal
from app.entities.enums import RequestStatus, TripStatus
from app.entities.requests import schemas
from app.entities.requests.calc.cost_calc import calculate_cost
from app.entities.trip.crud import TripCrud


def _model_to_schema(db_item: models.Chat) -> Optional[schemas.RequestReturn]:
    if db_item is None:
        return None
    return schemas.RequestReturn.model_validate(db_item.__dict__)


def _models_to_schema(db_items: list[models.Chat]) -> list[schemas.RequestReturn]:
    return [_model_to_schema(db_item) for db_item in db_items]


class RequestCrud:
    def __init__(self, db: SessionLocal):
        self.db = db

    def find_for_trip_id(self, trip_id: int) -> list[models.Request]:
        return self.db.query(models.Request).filter(models.Request.trip_id == trip_id).all()

    def find_for_trip_id_and_status(self, trip_id: int, status: RequestStatus) -> list[models.Request]:
        return (self.db.query(models.Request).
                filter(models.Request.trip_id == trip_id).
                filter(models.Request.status == status).all())

    def create(self, req: schemas.Request, user_id: int):
        trip = TripCrud(self.db).get_by_id(req.trip_id)
        # trip.update_trip(self.db)
        # Проверяем статус поездки
        if trip.status not in (TripStatus.NEW, TripStatus.BRONED):
            raise ValueError("Trip status must be 'NEW' or 'BRONED' to create a request")

        # Проверяем, достаточно ли свободных мест для создания нового запроса
        # TODO

        #if req.number_of_seats > trip.db_entity.available_seats:
        #    raise ValueError("Not enough available seats to create this request")8from 
        cost = calculate_cost(trip.id, req.departure_id, req.arrival_id, req.number_of_seats, self.db)

        new_request = models.Request(
            request_datetime=datetime.datetime.now(),
            status=RequestStatus.CREATED,
            status_change_datetime=datetime.datetime.now(),
            cost=cost,
            number_of_seats=req.number_of_seats,
            departure_id=req.departure_id,
            arrival_id=req.arrival_id,
            user_id=user_id,
            trip_id=req.trip_id
        )

        self.db.add(new_request)
        self.db.commit()
        self.db.refresh(new_request)
        return new_request
