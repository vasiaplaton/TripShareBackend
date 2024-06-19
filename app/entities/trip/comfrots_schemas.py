from pydantic import BaseModel


class ComfortsInTrip(BaseModel):
    max_two_passengers_in_the_back_seat: bool
    smoking_allowed: bool
    pets_allowed: bool
    free_trunk: bool