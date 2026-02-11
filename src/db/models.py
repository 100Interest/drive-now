from enum import Enum

from sqlalchemy import Column, ForeignKey, Integer, String, Enum as SQLAlchemyEnum, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

DeclarativeBase = declarative_base()


class CarStatus(Enum):
    AVAILABLE = "AVAILABLE"
    IN_USE = "IN_USE"
    UNDER_MAINTENANCE = "UNDER_MAINTENANCE"


class Car(DeclarativeBase):
    __tablename__ = "cars"
    id = Column(Integer, primary_key=True)
    model = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    status = Column(SQLAlchemyEnum(CarStatus), default=CarStatus.AVAILABLE)
    rentals = relationship("Rental", back_populates="car")


class Rentals(DeclarativeBase):
    __tablename__ = "rentals"
    id = Column(Integer, primary_key=True)
    car_id = Column(Integer, ForeignKey("cars.id"))
    customer_name = Column(String, nullable=False)
    rental_start_date = Column(DateTime, nullable=False)
    rental_end_date = Column(DateTime, nullable=False)
    car = relationship("Car", back_populates="rentals")
