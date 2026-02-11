import datetime
from typing import Optional

from src.db.models import Rental, Car, CarStatus
from src.db.session import Session


class RentalService:
    def __init__(self, db: Session):
        self.db = db

    def create_new_rental(self, car_id: int, customer_name: str) -> Rental:
        car = self.db.query(Car).filter(Car.id == car_id, Car.status == CarStatus.AVAILABLE).first()
        if not car:
            raise ValueError(f"Car with id {car_id} is not available")
        car.status = CarStatus.IN_USE
        rental = Rental(car_id=car_id, customer_name=customer_name)
        self.db.add(rental)
        self.db.commit()
        self.db.refresh(rental)
        return rental

    def end_rental(self, rental_id: int, end_date: Optional[datetime.datetime] = None) -> Rental:
        rental = self.db.query(Rental).filter(Rental.id == rental_id).first()
        if not rental:
            raise ValueError(f"Rental with id {rental_id} is not found")
        if rental.end_date:
            raise ValueError(f"Rental with id {rental_id} already ended")

        rental.end_date = end_date or datetime.datetime.now(datetime.UTC)
        rental.car.status = CarStatus.AVAILABLE
        self.db.commit()
        self.db.refresh(rental)
        return rental
