from typing import Optional

from src.db.models import Car, CarStatus
from src.db.session import Session


class CarService:
    def __init__(self, db: Session):
        self.db = db

    def add_car(self, model: str, year: int) -> Car:
        car = Car(model=model, year=year)
        self.db.add(car)
        self.db.commit()
        self.db.refresh(car)
        return car

    def get_car_by_id(self, car_id: int) -> Car | None:
        return self.db.query(Car).filter(Car.id == car_id).first()

    def update_car_status_by_car_id(self, car_id: int, new_status: CarStatus) -> Car:
        car = self.get_car_by_id(car_id)
        if not car:
            raise ValueError(f"No car with id {car_id} was found")
        car.status = new_status
        self.db.commit()
        self.db.refresh(car)
        return car

    def list_cars(self, status: Optional[CarStatus] = None, limit: Optional[int] = 10) -> list[Car]:
        query = self.db.query(Car)
        if status:
            query = query.filter(Car.status == status)
        query = query.limit(limit)
        return query.all()
