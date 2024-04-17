from sqlalchemy import DateTime, ForeignKey, Boolean, BigInteger, Column, Integer, String, Enum

from .database import Base
from .enums import TripStatus, RequestStatus, PaymentStatus


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    phone = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)

    name = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)

    # favorite genres
    talkativeness = Column(Integer, nullable=True)
    attitude_towards_smoking = Column(Integer, nullable=True)
    attitude_towards_animals_during_the_trip = Column(Integer, nullable=True)

    avatar_name = Column(String, nullable=False)


class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True)

    user_id_1 = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
    user_id_2 = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True)

    text = Column(String, nullable=True)
    image_path = Column(String, nullable=True)

    sender_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
    chat_id = Column(Integer, ForeignKey("chats.id", ondelete='CASCADE'), nullable=False)


class Stop(Base):
    __tablename__ = "stops"

    id = Column(Integer, primary_key=True)

    place = Column(String, nullable=False)
    place_name = Column(String, nullable=False)
    datetime = Column(DateTime, nullable=False)

    is_start = Column(Boolean, nullable=False)
    is_stop = Column(Boolean, nullable=False)
    num = Column(Integer, nullable=False)

    trip_id = Column(Integer, ForeignKey("trips.id", ondelete='CASCADE'), nullable=False)


class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True)

    max_passengers = Column(Integer, nullable=False)

    cost_sum = Column(Integer, nullable=False)

    max_two_passengers_in_the_back_seat = Column(Boolean, nullable=False)
    smoking_allowed = Column(Boolean, nullable=False)
    e_cigarettes_allowed = Column(Boolean, nullable=False)
    pets_allowed = Column(Boolean, nullable=False)
    free_trunk = Column(Boolean, nullable=False)
    status = Column(Enum(TripStatus), nullable=False)

    car_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
    driver_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)


class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True)

    brand = Column(String, nullable=False)
    mode = Column(String, nullable=False)
    color = Column(String, nullable=False)
    year_of_manufacture = Column(Integer, nullable=False)
    photo = Column(String, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)


class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True)

    request_datetime = Column(DateTime, nullable=False)
    status = Column(Enum(RequestStatus), nullable=False)
    status_change_datetime = Column(DateTime, nullable=True)
    cost = Column(Integer, nullable=False)
    number_of_seats = Column(Integer, nullable=False)

    departure_id = Column(Integer, ForeignKey("stops.id", ondelete='CASCADE'), nullable=False)
    arrival_id = Column(Integer, ForeignKey("arrival.id", ondelete='CASCADE'), nullable=False)

    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
    trip_id = Column(Integer, ForeignKey("trips.id", ondelete='CASCADE'), nullable=False)


class Review(Base):
    id = Column(Integer, primary_key=True)

    text = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)

    writer_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)


class PaymentMethod(Base):
    id = Column(Integer, primary_key=True)

    data_json = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)


class Payment(Base):
    id = Column(Integer, primary_key=True)

    amount = Column(Integer, primary_key=True)
    status = Column(Enum(PaymentStatus), nullable=False)



    """
     * id: int <<PK>>
  * amount: int
  --
  * amount: int
  * status: enum [CREATED, OK, RETURNED]
  __
  * payment_id: int <<FK>>
  * request_id: int <<FK>>
  * user_id: int <<FK>>
    """


"""
entity User {
  * id: int: <<PK>>
  --
  * phone: str
  * password_hash: str

  * name: str
  * rating: double
  * favorite_genres: list[str]

  talkativeness: int 0-10
  attitude towards smoking: int 0-10
  attitude towards animals during the trip: int 0-10

  avatar: path to file
  __

}

entity Trip {
  * id: int <<PK>>
  --
  * departure_place: geo
  * departure_datetime: datetime
  * arrival_place: geo
  * arrival_datetime: datetime
  * max_passengers

  * cost: int
  * stops: list[?]

  max two passengers in the back seat: bool
  smoking_allowed: bool
  e-cigarettes_allowed: bool
  pets_allowed: bool
  free_trunk: bool
  status: enum [New, Broned, FullyBronned, InProgress, Finished]
  __
  * car_id <<FK>>
  * driver_id <<FK>>
}

entity Car {
  * id: int <<PK>>
  --
  * brand: str
  * model: str
  * color: rgb
  * year_of_manufacture: int
  * photo: list[path]

  __
  * user_id: int <<FK>>
}

entity Request {
  * id: int <<PK>>
  --
  * request_datetime: datetime
  * status: enum(Created, Accepted, Declined, Finished)
  * status_change_datetime: datetime
  * cost: int
  * number_of_seats: int

  * departure: geo
  * arrival: geo
  __
  * trip_id: int <<FK>>
  * user_id: int <<FK>>
}

User ||..o{ Car
Trip ||..|| Car
Trip ||..|| User
Trip ||..o{ Request
User ||..o{ Request


entity Chat {
  * id <<PK>>
  --
  __
 * user_id_1 <<FK>>
 * user_id_2 <<FK>>
}

entity ChatMessage {
  * id <<PK>>
  --
  text: str
  img: path
  __
  * sender_id <<FK>>
  * chat_id <<FK>>
}

User ||..o{ Chat
ChatMessage ||..|| User
ChatMessage ||..|| User

entity Review {
 * id <<PK>>
 --
 text: str
 rating: int
 __
 * writer_id: int <<FK>>
 * user_id: int <<FK>>
}

Review ||..|| User
Review ||..|| User

entity Payment {
  * id: int <<PK>>
  * amount: int
  --
  * amount: int
  * status: enum [CREATED, OK, RETURNED]
  __
  * payment_id: int <<FK>>
  * request_id: int <<FK>>
  * user_id: int <<FK>>
}

Payment ||..|| User
Payment ||..|| Request


entity PaymentMethod {
  * id: int <<PK>>
  --
  * data_json: str[json]
  __
  * user_id <<FK>>
}

User ||..o{ PaymentMethod

@enduml

"""
