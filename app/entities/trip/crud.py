from typing import Optional

from app.database import models
from app.database.database import SessionLocal
from app.entities.enums import TripStatus
from app.entities.exceptions import ValidateError
from app.entities.trip import schemas, stop_crud
from app.entities.trip.stop_crud import StopCrud


def _model_to_schema(db_item: models.Trip, db: SessionLocal) -> Optional[schemas.TripReturn]:
    if db_item is None:
        return None
    db.commit()
    stops = StopCrud(db).get_stops_by_trip_id(db_item.id)
    stops = stop_crud._models_to_schema(stops)
    d = db_item.__dict__
    d["stops"] = stops
    # TODO add stops
    return schemas.TripReturn.model_validate(d)


def _models_to_schema(db_items: list[models.Trip], db: SessionLocal) -> list[schemas.TripReturn]:
    return [_model_to_schema(db_item, db) for db_item in db_items]


class TripCrud:
    def __init__(self, db: SessionLocal):
        self.db = db

    def create(self, schema: schemas.TripCreate, driver_id: int):
        db_trip = models.Trip(
            **schema.dict(exclude={"stops"}),
            driver_id=driver_id,
            status=TripStatus.NEW,
        )

        self.db.add(db_trip)
        self.db.flush()
        self.db.refresh(db_trip)

        stops = schema.stops
        if len(stops) < 2:
            raise ValidateError()

        stops.sort(key=lambda stop: stop.num)

        for i, stop in enumerate(stops):
            num = i
            is_start = i == 0
            is_stop = i == len(stops) - 1
            StopCrud(self.db).create(
                schemas.Stop(
                    **stop.model_dump(exclude={"num"})
                    , num=num
                ),
                is_start=is_start,
                is_stop=is_stop,
                trip_id=db_trip.id,
                commit=False
            )

        self.db.commit()

        return db_trip

    def get_by_driver_id(self, driver_id: int) -> list[models.Trip]:
        return self.db.query(models.Trip).filter(models.Trip.driver_id == driver_id).all()
