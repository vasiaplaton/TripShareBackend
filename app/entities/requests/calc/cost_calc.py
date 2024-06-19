from app.database.database import SessionLocal
from app.entities.requests.calc.validator_stops import validate_all


def calculate_cost(trip_id: int, start_id: int, stop_id: int, seats: int, db: SessionLocal):
    trip, start, stop, all_stops = validate_all(trip_id, start_id, stop_id, db)

    lenn = stop.num - start.num + 1
    return int((lenn / len(all_stops)) * trip.cost_sum * seats / trip.max_passengers)