import logging
from typing import Optional

from src.db.models import Car, CarStatus
from src.db.session import Session
from src.metrics import count_car_added

logger = logging.getLogger(__name__)


class CarService:
    """
    Service layer for managing car-related operations

    Encapsulates database access and business logic for creating,
    retrieving, updating, and listing cars
    """

    def __init__(self, db: Session):
        """
        Initialize the service with an active database session

        Args:
            db (Session): SQLAlchemy session injected (via FastAPI "Depends" Injection)
       """
        self.db = db

    def add_car(self, model: str, year: int) -> Car:
        """
         Create and persist a new car

         Args:
             model (str): Car model name
             year (int): Manufacturing year

         Returns:
             Car: The newly created car after commit and refresh
         """
        car = Car(model=model, year=year)
        self.db.add(car)
        self.db.commit()
        self.db.refresh(car)

        count_car_added(model)
        logger.info(f"New car added model: {model} year: {year}")
        return car

    def get_car_by_id(self, car_id: int) -> Car | None:
        """
        Retrieve a car by its ID

        Args:
            car_id (int): Unique identifier of the car

        Returns:
            Car | None: The car if found, otherwise None
        """
        return self.db.query(Car).filter(Car.id == car_id).first()

    def update_car_status_by_car_id(self, car_id: int, new_status: CarStatus) -> Car:
        """
        Update the status of a car by its ID

        Args:
            car_id (int): Unique identifier of the car
            new_status (CarStatus): New status to assign

        Returns:
            Car: The updated car.

        Raises:
            ValueError: If no car with the given ID exists
        """
        car = self.get_car_by_id(car_id)
        if not car:
            logger.info(f"No car with the given ID found car_id={car_id}")
            raise ValueError(f"No car with id {car_id} was found")
        previous_status = car.status
        car.status = new_status
        self.db.commit()
        self.db.refresh(car)
        logger.info(f"Car status updated previous_status: {previous_status} new_status: {new_status}")
        return car

    def list_cars(self, status: Optional[CarStatus] = None, limit: Optional[int] = 10) -> list[Car]:
        """
        List cars with optional status filtering and result limiting

        Args:
            status (Optional[CarStatus]): Filter cars by status
            limit (Optional[int]): Maximum number of results to return

        Returns:
            list[Car]: List of matching cars
        """
        query = self.db.query(Car)
        if status:
            query = query.filter(Car.status == status)
        query = query.limit(limit)
        return query.all()
