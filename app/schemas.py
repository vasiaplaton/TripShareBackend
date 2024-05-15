from pydantic import BaseModel


"""
class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True)

    request_datetime = Column(DateTime, nullable=False)
    status = Column(Enum(RequestStatus), nullable=False)
    status_change_datetime = Column(DateTime, nullable=True)
    cost = Column(Integer, nullable=False)
    number_of_seats = Column(Integer, nullable=False)

    departure_id = Column(Integer, ForeignKey("stops.id", ondelete='CASCADE'), nullable=False)
    arrival_id = Column(Integer, ForeignKey("stops.id", ondelete='CASCADE'), nullable=False)

    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
    trip_id = Column(Integer, ForeignKey("trips.id", ondelete='CASCADE'), nullable=False)


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)

    text = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)

    writer_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)


class PaymentMethod(Base):
    __tablename__ = "payment_methods"

    id = Column(Integer, primary_key=True)

    data_json = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)

    amount = Column(Integer, primary_key=True)
    status = Column(Enum(PaymentStatus), nullable=False)

    payment_method_id = Column(Integer, ForeignKey("payment_methods.id", ondelete='CASCADE'), nullable=False)
    request_id = Column(Integer, ForeignKey("requests.id", ondelete='CASCADE'), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
"""
