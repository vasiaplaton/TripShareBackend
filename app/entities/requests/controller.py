import datetime

from fuzzywuzzy import fuzz

from app.database.database import SessionLocal
from app.entities.enums import RequestStatus, TripStatus
from app.entities.exceptions import NotFound, ValidateError
from app.entities.places.crud import PlacesCrud
from app.entities.requests.calc.cost_calc import calculate_cost
from app.entities.requests.calc.dist_calc import compare_places
from app.entities.requests.calc.validator_stops import validate_all
from app.entities.requests.crud import RequestCrud
from app.entities.requests.schemas import FindRequest, FindResult
from app.entities.trip.crud import TripCrud
from app.entities.trip import stop_crud, crud as trip_crud
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
    trip, start, stop, all_stops = validate_all(trip_id, start_id, stop_id, db)

    requests = find_for_trip_in_between(trip_id, start.num, stop.num, RequestStatus.ACCEPTED, db)
    requests += find_for_trip_in_between(trip_id, start.num, stop.num, RequestStatus.PAYED, db)
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


def find_trip(req: FindRequest, db: SessionLocal):
    request_start = req.start
    request_stop = req.end
    date_to_find = req.date

    trips = TripCrud(db).find_for_status([TripStatus.NEW, TripStatus.BRONED])
    res = []
    for trip in trips:
        print("AAA")
        stops = StopCrud(db).get_stops_by_trip_id(trip.id)

        max_good_start = None
        max_good_start_rated = 100
        for stop_l in stops:
            rate = compare_places(
                Place(place=stop_l.place, place_name=stop_l.place_name),
                request_start,
                db
            )
            print(f"Rete {rate}")
            if date_to_find.date() != stop_l.datetime.date():
                print(f"Skipping by date, {date_to_find.date()} {stop_l.datetime.date()}")
                continue

            if rate <= max_good_start_rated:
                max_good_start_rated = rate
                max_good_start = stop_l

        if not max_good_start:
            continue

        print("Found start")

        max_good_end = None
        max_good_end_rated = 100
        for stop_l in stops[max_good_start.num + 1:]:
            rate = compare_places(
                Place(place=stop_l.place, place_name=stop_l.place_name),
                request_stop,
                db
            )
            print(f"Rete {rate}")

            if rate <= max_good_end_rated:
                max_good_end_rated = rate
                max_good_end = stop_l

        if not max_good_end:
            continue

        print("FOUND^ check spaces")
        free_spaces = find_free_spaces(trip.id, max_good_start.id, max_good_end.id, db)
        print(free_spaces)

        if req.needed_seats > free_spaces:
            continue

        res.append(FindResult(
            start_distance=int(max_good_start_rated),
            start=stop_crud._model_to_schema(max_good_start).model_dump(),
            end_distance=int(max_good_end_rated),
            end=stop_crud._model_to_schema(max_good_end).model_dump(),
            trip=trip_crud._model_to_schema(trip, db).model_dump(),
            cost=calculate_cost(trip.id, max_good_start.id, max_good_end.id, req.needed_seats, db)
            )
        )

    return res
