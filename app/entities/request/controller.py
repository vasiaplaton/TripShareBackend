from . import schemas, models
from ...controllers.exceptions import NotFound
from ...database import SessionLocal


class Request:
    model = models.Request
    db = SessionLocal()
