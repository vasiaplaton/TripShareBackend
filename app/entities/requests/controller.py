import datetime

from fuzzywuzzy import fuzz

from app.database.database import SessionLocal
from app.entities.enums import RequestStatus, TripStatus
from app.entities.exceptions import NotFound, ValidateError
from app.entities.requests.crud import RequestCrud
from app.entities.trip.crud import TripCrud
from app.entities.trip.schemas import Stop, Place
from app.entities.trip.stop_crud import StopCrud


def find_for_trip_in_between(trip_id: int, start_num: int, stop_num: int, status: RequestStatus,
                             db: SessionLocal):
    res = []
    for request in RequestCrud(db).find_for_trip_id_and_status(trip_id, status):
        start = StopCrud(db).get_by_id(request.departure_id)
        # stop = StopCrud(db).get_by_id(request.arrival_id)
        if start_num <= start.num < stop_num:
            res.append(request)

    return res


def find_free_spaces(trip_id: int, start_id: int, stop_id: int, db: SessionLocal):
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
    all_stops.sort(key=lambda l: l.num)

    requests = find_for_trip_in_between(trip_id, start.num, stop.num, RequestStatus.ACCEPTED, db)

    occupied = 0
    for stop_needed in all_stops[start.num:stop.num]:
        summm = 0
        for request in requests:
            start = StopCrud(db).get_by_id(request.departure_id)
            stop = StopCrud(db).get_by_id(request.arrival_id)
            if start.num <= stop_needed.num <= stop.num:
                summm += request.number_of_seats
        occupied = max(occupied, summm)
        # find all accepted requests

    return trip.max_passengers - occupied


def compare_places(one: Place, two: Place):
    return 100 - int(fuzz.ratio(one.place_name, two.place_name))


def find_trip(start: Place, stop: Place, start_date: datetime.datetime, needed_seats: int, db: SessionLocal):
    trips = TripCrud(db).find_for_status([TripStatus.NEW, TripStatus.BRONED])
    res = []
    for trip in trips:
        stops = StopCrud(db).get_stops_by_trip_id(trip.id)

        max_good = None
        max_good_rated = 0
        for stop_l in stops:
            rate = compare_places(
                Place(place=stop_l.place, place_name=stop_l.place_name),
                start
            )
            if start_date.date() != stop_l.date():
                continue

            if rate < max_good_rated:
                max_good_rated = rate
                max_good = stop_l

        if not max_good:
            continue

        max_good_end = None
        max_good_end_rated = 0
        for stop_l in stops[max_good.num+1:]:
            rate = compare_places(
                Place(place=stop_l.place, place_name=stop_l.place_name),
                stop
            )

            if rate < max_good_end_rated:
                max_good_end_rated = rate
                max_good_end = stop_l

        if not max_good_end:
            continue

        res.append(
            {"start_distance": max_good_rated,
             "start": max_good.id,
             "end_distance": max_good_end_rated,
             "end": max_good_end.id}
        )

    return res
