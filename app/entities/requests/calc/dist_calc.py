from geopy.distance import distance

from app.database.database import SessionLocal
from app.entities.exceptions import ValidateError
from app.entities.places.crud import PlacesCrud
from app.entities.trip.schemas import Place


def compare_places(one: Place, two: Place, db: SessionLocal):
    one_data = PlacesCrud(db).get_by_id(int(one.place))
    if not one_data:
        raise ValidateError

    two_data = PlacesCrud(db).get_by_id(int(two.place))
    if not two_data:
        raise ValidateError

    # Координаты первой точки (широта, долгота)
    coords1 = (one_data.latitude_dd, one_data.longitude_dd)

    # Координаты второй точки (широта, долгота)
    coords2 = (two_data.latitude_dd, two_data.longitude_dd)

    # Вычисление расстояния между точками
    dist_km = distance(coords1, coords2).kilometers

    return dist_km

