import random
from datetime import datetime

from app.database import SessionLocal
from app.entities.enums import RequestStatus
from app.entities.request import models
from app.entities.request.schemas import RequestCreate
from app.entities.trip import models as trip_models


class RequestCRUD:
    def __init__(self, db: SessionLocal):
        self.db = db

    def create(self, req: RequestCreate):
        # Получаем информацию о поездке
        trip = self.db.query(trip_models.Trip).get(req.trip_id)
        if not trip:
            raise ValueError("Trip with id {} not found".format(req.trip_id))

        # Проверяем статус поездки
        if trip.status not in (trip_models.TripStatus.NEW.value, trip_models.TripStatus.BRONED.value):
            raise ValueError("Trip status must be 'NEW' or 'BRONED' to create a request")

        # Получаем все запросы для данной поездки со статусом "ACCEPTED" или "CREATED"
        requests = self.get_requests_by_trip_id(req.trip_id, status=RequestStatus.ACCEPTED.value)

        # Подсчитываем количество занятых мест
        occupied_seats = sum(req.number_of_seats for req in requests)

        # Подсчитываем количество свободных мест
        available_seats = trip.max_passengers - occupied_seats

        # Проверяем, достаточно ли свободных мест для создания нового запроса
        if req.number_of_seats > available_seats:
            raise ValueError("Not enough available seats to create this request")

        new_request = models.Request(
            request_datetime=datetime.now(),
            status=RequestStatus.CREATED,
            status_change_datetime=datetime.now(),
            cost=req.cost,
            number_of_seats=req.number_of_seats,
            departure_id=req.departure_id,
            arrival_id=req.arrival_id,
            user_id=req.user_id,
            trip_id=req.trip_id
        )

        self.db.add(new_request)
        self.db.commit()
        self.db.refresh(new_request)
        return new_request

    def get_requests_by_trip_id(self, trip_id: int, status: str = None) -> list[models.Request]:
        query = self.db.query(models.Request).filter(models.Request.trip_id == trip_id)
        if status:
            query = query.filter(models.Request.status == status)
        return query.all()

    def update_request_status(self, request_id: int, new_status: str):
        request = self.db.query(models.Request).get(request_id)
        if not request:
            raise ValueError("Request with id {} not found".format(request_id))

        # Получаем информацию о поездке
        trip = self.db.query(trip_models.Trip).get(request.trip_id)
        if not trip:
            raise ValueError("Trip with id {} not found".format(request.trip_id))

        # Проверяем статус поездки
        if trip.status not in (trip_models.TripStatus.NEW.value, trip_models.TripStatus.BRONED.value):
            raise ValueError("Trip status must be 'NEW' or 'BRONED' to update request status")

        # Если новый статус запроса - "ACCEPTED"
        if new_status == models.RequestStatus.ACCEPTED.value:
            self.accept_request(request, trip)

            # Если новый статус запроса - "DECLINED"
        elif new_status == models.RequestStatus.DECLINED.value:
            # Обновляем статус запроса на "DECLINED"
            request.status = models.RequestStatus.DECLINED.value
            self.db.commit()
        # Если новый статус запроса - "FINISHED"
        elif new_status == models.RequestStatus.FINISHED.value:
            # Обновляем статус запроса на "FINISHED"
            request.status = models.RequestStatus.FINISHED.value
            self.db.commit()

        self.db.refresh(request)
        return request

    def accept_request(self, request: models.Request, trip: trip_models.Trip):
        # Получаем все запросы для данной поездки со статусом "ACCEPTED" или "CREATED"
        requests = self.get_requests_by_trip_id(request.trip_id, status=RequestStatus.ACCEPTED.value)
        # Подсчитываем количество занятых мест
        occupied_seats = sum(req.number_of_seats for req in requests)
        # Подсчитываем количество свободных мест
        available_seats = trip.max_passengers - occupied_seats
        # Проверяем, достаточно ли свободных мест для подтверждения запроса
        if request.number_of_seats > available_seats:
            raise ValueError("Not enough available seats to accept this request")
        # Если после подтверждения статус поездки был NEW, меняем его на BRONED
        if trip.status == trip_models.TripStatus.NEW.value:
            trip.status = trip_models.TripStatus.BRONED.value
            self.db.commit()
            self.db.refresh(trip)

        available_seats -= request.number_of_seats
        # Если свободных мест не осталось, меняем статус поездки на FULLY_BRONNED
        if available_seats == 0:
            trip.status = trip_models.TripStatus.FULLY_BRONNED.value
            # Отклоняем все остальные запросы
            for req in requests:
                if req.id == request.id:
                    continue
                if req.status == RequestStatus.CREATED:
                    req.status = models.RequestStatus.DECLINED.value
                    self.db.commit()
        # Обновляем статус запроса на "ACCEPTED"
        request.status = models.RequestStatus.ACCEPTED.value
        self.db.commit()

    def get_requests_by_user_id(self, user_id: int) -> list[models.Request]:
        query = self.db.query(models.Request).filter(models.Request.user_id == user_id)
        return query.all()
