import datetime
from typing import Optional

from pydantic import BaseModel

from app.entities.enums import PaymentStatus


class Pay(BaseModel):
    amount: int
    status: PaymentStatus

    datetime_cr: datetime.datetime
    datetime_fn: Optional[datetime.datetime] = None
    from_user_id: int
    to_user_id: int

    trip_id: int
    request_id: int


class PayReturn(Pay):
    id: int