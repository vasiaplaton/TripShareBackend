import enum


class TripStatus(str, enum.Enum):
    NEW = "NEW"
    BRONED = "BRONED"
    FULLY_BRONNED = "FULLY_BRONNED"
    IN_PROGRESS = "IN_PROGRESS"
    FINISHED = "FINISHED"


class RequestStatus(str, enum.Enum):
    CREATED = "CREATED"
    ACCEPTED = "ACCEPTED"
    DECLINED = "DECLINED"
    PAYED = "PAYED"
    FINISHED = "FINISHED"
    ERROR = "ERROR"


class PaymentStatus(str, enum.Enum):
    CREATED = "CREATED"
    OK = "OK"
    ERROR = "ERROR"
    RETURNED = "RETURNED"
