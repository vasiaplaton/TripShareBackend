import datetime
from typing import Optional

from sqlalchemy import or_

from app.database import models
from app.database.database import SessionLocal
from app.entities.enums import RequestStatus, TripStatus, PaymentStatus
from app.entities.exceptions import NotFound, ValidateError
from app.entities.pays.crud import PaysCrud
from app.entities.pays.schemas import Pay
from app.entities.requests import schemas
from app.entities.requests.calc.cost_calc import calculate_cost
from app.entities.trip.crud import TripCrud
from app.entities.user.crud import UserCrud
from app.entities.user import crud as user_crud

def _model_to_schema(db_item: models.Request) -> Optional[schemas.RequestReturn]:
    if db_item is None:
        return None
    return schemas.RequestReturn.model_validate(db_item.__dict__)


def _models_to_schema(db_items: list[models.Request]) -> list[schemas.RequestReturn]:
    return [_model_to_schema(db_item) for db_item in db_items]


def _model_to_schema_user(db_item: models.Request, db) -> Optional[schemas.RequestReturnUser]:
    if db_item is None:
        return None
    d = db_item.__dict__
    d["user"] = user_crud._model_to_schema(UserCrud(db).get_user_by_id(db_item.user_id), db, car_dto=False)
    return schemas.RequestReturnUser.model_validate(d)


def _models_to_schema_user(db_items: list[models.Request], db) -> list[schemas.RequestReturnUser]:
    return [_model_to_schema_user(db_item, db) for db_item in db_items]


class RequestCrud:
    def __init__(self, db: SessionLocal):
        self.db = db

    def find_for_id(self, id: int) -> models.Request:
        return self.db.query(models.Request).filter(models.Request.id == id).first()

    def find_for_trip_id(self, trip_id: int) -> list[models.Request]:
        return self.db.query(models.Request).filter(models.Request.trip_id == trip_id).all()

    def find_for_user_id(self, user_id: int) -> list[models.Request]:
        return self.db.query(models.Request).filter(models.Request.user_id == user_id).all()

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

        # if req.number_of_seats > trip.db_entity.available_seats:
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

    def update_status(self, req_id: int, status: RequestStatus, user_id: int):
        req = self.find_for_id(req_id)
        if req is None:
            raise NotFound()

        trip = TripCrud(self.db).get_by_id(req.trip_id)

        if status in [RequestStatus.ACCEPTED, RequestStatus.DECLINED, RequestStatus.FINISHED, RequestStatus.ERROR]:
            if trip.driver_id != user_id:
                raise ValidateError()

            # TODO check free spaces
            req.status = status

            if status == RequestStatus.ACCEPTED:
                req.status = RequestStatus.PAYED
                PaysCrud(self.db).create(
                    Pay(
                        amount=req.cost,
                        status=PaymentStatus.CREATED,
                        datetime_cr=datetime.datetime.now(),
                        from_user_id=req.user_id,
                        to_user_id=trip.driver_id,
                        trip_id=trip.id,
                        request_id=req.id
                    )
                )

            elif status == RequestStatus.FINISHED:
                res = PaysCrud(self.db).get_for_request(request_id=req.id)
                if res:
                    res.status = PaymentStatus.OK

            elif status == RequestStatus.ERROR or status == RequestStatus.DECLINED:
                res = PaysCrud(self.db).get_for_request(request_id=req.id)
                if res:
                    res.status = PaymentStatus.RETURNED

            self.db.commit()
