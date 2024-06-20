from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.entities.enums import RequestStatus, TripStatus
from app.entities.exceptions import NotFound
from app.entities.requests import schemas
from app.entities.requests.controller import find_trip
from app.entities.requests.crud import RequestCrud, _model_to_schema, _models_to_schema, _models_to_schema_user
from app.entities.requests.schemas import RequestReturn, FindResult, FindRequest, RequestReturnWithTrip
from app.entities.trip.crud import TripCrud
from app.entities.trip import crud as trip_crud
from app.entities.user.crud import get_current_user
from app.entities.user.schemas import UserReturn

request_router = APIRouter(
    prefix="/requests",
    tags=["requests"]
)


@request_router.post("/me", response_model=RequestReturn)
def create_request(req: schemas.Request,
                   current_user: Annotated[UserReturn, Depends(get_current_user)],
                   db: Session = Depends(get_db)):
    return _model_to_schema(RequestCrud(db).create(req, user_id=current_user.id))


@request_router.post("/for_trip/{trip_id}", response_model=RequestReturn)
def find_for_trip_request(trip_id: int,
                   current_user: Annotated[UserReturn, Depends(get_current_user)],
                   db: Session = Depends(get_db)):
    return _models_to_schema_user(RequestCrud(db).find_for_trip_id(trip_id=trip_id), db)


@request_router.post("/find", response_model=list[FindResult])
def find_trips_route(req: FindRequest, db: Session = Depends(get_db)):
    return find_trip(req, db)


@request_router.post("/accept/{request_id}")
def accept_request(request_id: int,
                   current_user: Annotated[UserReturn, Depends(get_current_user)],
                   db: Session = Depends(get_db)):
    RequestCrud(db).update_status(req_id=request_id, status=RequestStatus.ACCEPTED, user_id=current_user.id)


@request_router.post("/decline/{request_id}")
def decline_request(request_id: int,
                    current_user: Annotated[UserReturn, Depends(get_current_user)],
                    db: Session = Depends(get_db)):
    RequestCrud(db).update_status(req_id=request_id, status=RequestStatus.DECLINED, user_id=current_user.id)


@request_router.post("/finish_trip/{trip_id}")
def finish_trip(trip_id: int,
                    current_user: Annotated[UserReturn, Depends(get_current_user)],
                    db: Session = Depends(get_db)):
    res = TripCrud(db).get_by_id(trip_id)
    if not res:
        raise NotFound
    if not res.driver_id == current_user.id:
        raise

    res.status = TripStatus.FINISHED
    for i in RequestCrud(db).find_for_trip_id(res.id):
        RequestCrud(db).update_status(i.id, RequestStatus.FINISHED, current_user.id)


@request_router.post("/error_trip_id/{trip_id}")
def finish_trip_error(trip_id: int,
                current_user: Annotated[UserReturn, Depends(get_current_user)],
                db: Session = Depends(get_db)):
    res = TripCrud(db).get_by_id(trip_id)
    if not res:
        raise NotFound
    if not res.driver_id == current_user.id:
        raise

    res.status = TripStatus.FINISHED
    for i in RequestCrud(db).find_for_trip_id(res.id):
        RequestCrud(db).update_status(i.id, RequestStatus.ERROR, current_user.id)


@request_router.get("/me")
def get_my_requests(current_user: Annotated[UserReturn, Depends(get_current_user)],
                    db: Session = Depends(get_db)) -> list[RequestReturnWithTrip]:
    res = RequestCrud(db).find_for_user_id(current_user.id)
    res1 = []
    for r in res:
        print(TripCrud(db).get_by_id(r.trip_id).__dict__)
        res1.append(
            RequestReturnWithTrip(
                **r.__dict__,
                trip=trip_crud._model_to_schema(TripCrud(db).get_by_id(r.trip_id), db, stops_dto=True).model_dump()
            ))

    return res1
