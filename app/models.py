from sqlalchemy import DateTime, ForeignKey, Boolean, Column, Integer, String, Enum

from app.database import Base
from app.entities.enums import RequestStatus, PaymentStatus


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
