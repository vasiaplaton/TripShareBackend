from app.database.database import SessionLocal
from app.entities.exceptions import NotFound, ValidateError
from app.entities.trip.crud import TripCrud
from app.entities.trip.stop_crud import StopCrud


def validate_all(trip_id: int, start_id: int, stop_id: int, db: SessionLocal):
    trip = TripCrud(db).get_by_id(trip_id)
    if not trip:
        raise NotFound()

    start = StopCrud(db).get_by_id(start_id)
    if not start:
        raise NotFound("Cant found start")
    if start.trip_id != trip_id:
        raise ValidateError("Start not belongs to trip")

    stop = StopCrud(db).get_by_id(stop_id)
    if not stop:
        raise NotFound("Cant found stop")
    if stop.trip_id != trip_id:
        raise ValidateError("Stop not belongs to trip")

    all_stops = StopCrud(db).get_stops_by_trip_id(trip_id)
    return trip, start, stop, all_stops