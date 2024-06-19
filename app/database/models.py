from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey, DateTime, Float

from app.database.database import Base
from app.entities.enums import TripStatus, RequestStatus, PaymentStatus


class User(Base):
    __tablename__ = "users"
    __pk__ = "users.id"

    id = Column(Integer, primary_key=True, autoincrement=True)

    phone = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)

    name = Column(String, nullable=False)

    surname = Column(String, nullable=False)
    email = Column(String, nullable=True)
    birthday = Column(String, nullable=False)
    musicPreferences = Column(String, nullable=True)
    info = Column(String, nullable=True)

    rating = Column(Float, nullable=True)

    # favorite genres
    talkativeness = Column(Integer, nullable=True)
    attitude_towards_smoking = Column(Integer, nullable=True)
    attitude_towards_animals_during_the_trip = Column(Integer, nullable=True)

    avatar_url = Column(String, nullable=True)


class Car(Base):
    __tablename__ = "cars"
    __pk__ = "cars.id"

    id = Column(Integer, primary_key=True, autoincrement=True)

    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    color = Column(String, nullable=False)
    year_of_manufacture = Column(Integer, nullable=False)

    iamges_url = Column(String, nullable=True)

    user_id = Column(Integer, ForeignKey(User.__pk__, ondelete='CASCADE'), nullable=False)


class Trip(Base):
    __tablename__ = "trips"
    __pk__ = "trips.id"

    id = Column(Integer, primary_key=True, autoincrement=True)

    max_passengers = Column(Integer, nullable=False)

    cost_sum = Column(Integer, nullable=False)

    max_two_passengers_in_the_back_seat = Column(Boolean, nullable=False)
    smoking_allowed = Column(Boolean, nullable=False)
    pets_allowed = Column(Boolean, nullable=False)
    free_trunk = Column(Boolean, nullable=False)
    status = Column(Enum(TripStatus), nullable=False)

    car_id = Column(Integer, ForeignKey(Car.__pk__, ondelete='CASCADE'), nullable=False)
    driver_id = Column(Integer, ForeignKey(User.__pk__, ondelete='CASCADE'), nullable=False)


class Stop(Base):
    __tablename__ = "stops"
    __pk__ = "stops.id"

    id = Column(Integer, primary_key=True, autoincrement=True)

    place = Column(String, nullable=False)
    place_name = Column(String, nullable=False)
    datetime = Column(DateTime, nullable=False)

    is_start = Column(Boolean, nullable=False)
    is_stop = Column(Boolean, nullable=False)
    num = Column(Integer, nullable=False)

    trip_id = Column(Integer, ForeignKey(Trip.__pk__, ondelete='CASCADE'), nullable=False)


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, autoincrement=True)

    text = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)

    image_url = Column(String, nullable=True)
    writer_id = Column(Integer, ForeignKey(User.__pk__, ondelete='CASCADE'), nullable=False)
    user_id = Column(Integer, ForeignKey(User.__pk__, ondelete='CASCADE'), nullable=False)


class Request(Base):
    __tablename__ = "requests"
    __pk__ = "requests.id"
    id = Column(Integer, primary_key=True, autoincrement=True)

    request_datetime = Column(DateTime, nullable=False)
    status = Column(Enum(RequestStatus), nullable=False)
    status_change_datetime = Column(DateTime, nullable=True)
    cost = Column(Integer, nullable=False)
    number_of_seats = Column(Integer, nullable=False)

    departure_id = Column(Integer, ForeignKey(Stop.__pk__, ondelete='CASCADE'), nullable=False)
    arrival_id = Column(Integer, ForeignKey(Stop.__pk__, ondelete='CASCADE'), nullable=False)

    user_id = Column(Integer, ForeignKey(User.__pk__, ondelete='CASCADE'), nullable=False)
    trip_id = Column(Integer, ForeignKey(Trip.__pk__, ondelete='CASCADE'), nullable=False)


class Chat(Base):
    __tablename__ = "chats"
    __pk__ = "chats.id"

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id_1 = Column(Integer, ForeignKey(User.__pk__, ondelete='CASCADE'), nullable=False)
    user_id_2 = Column(Integer, ForeignKey(User.__pk__, ondelete='CASCADE'), nullable=False)


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, autoincrement=True)

    text = Column(String, nullable=True)

    created_at = Column(DateTime, nullable=False)

    image_url = Column(String, nullable=True)
    sender_id = Column(Integer, ForeignKey(User.__pk__, ondelete='CASCADE'), nullable=False)
    chat_id = Column(Integer, ForeignKey(Chat.__pk__, ondelete='CASCADE'), nullable=False)


class Pay(Base):
    __tablename__ = "pay"
    id = Column(Integer, primary_key=True, autoincrement=True)

    amount = Column(Integer, nullable=False)
    status = Column(Enum(PaymentStatus), nullable=False)
    from_user_id = Column(Integer, ForeignKey(User.__pk__, ondelete='CASCADE'), nullable=False)
    to_user_id = Column(Integer, ForeignKey(User.__pk__, ondelete='CASCADE'), nullable=False)

    trip_id = Column(Integer, ForeignKey(Trip.__pk__, ondelete='CASCADE'), nullable=False)
    request_id = Column(Integer, ForeignKey(Request.__pk__, ondelete='CASCADE'), nullable=False)