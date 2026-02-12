import datetime
import logging
from typing import Optional

from src.db.models import Rental, Car, CarStatus
from src.db.session import Session
from src.exceptions import CarUnavailableError, RentalNotFoundError, RentalAlreadyEndedError
from src.metrics import count_rental_created, count_rental_ended, update_gauges

logger = logging.getLogger(__name__)


class RentalService:
    """
    Service layer for handling rental lifecycle operations.

    Manages business logic for creating and ending rentals,
    including updating related car status.
    """

    def __init__(self, db: Session):
        """
        Initialize the service with an active database session.

        Args:
            db (Session): SQLAlchemy session injected (via FastAPI "Depends" Injection)
        """
        self.db = db

    def create_new_rental(self, car_id: int, customer_name: str) -> Rental:
        """
        Create a new rental for an available car

        Args:
            car_id (int): ID of the car to rent
            customer_name (str): Name of the customer renting the car

        Returns:
            Rental: The newly created rental record

        Raises:
            ValueError: If the car does not exist or is not available
        """
        car = self.db.query(Car).filter(Car.id == car_id, Car.status == CarStatus.AVAILABLE).first()
        if not car:
            logger.info(f"Car is not ready for use yet car_id={car_id}")
            raise CarUnavailableError(car_id)
        car.status = CarStatus.IN_USE
        rental_start_date = datetime.datetime.now(datetime.UTC)
        rental = Rental(car_id=car_id, customer_name=customer_name,
                        rental_start_date=rental_start_date, rental_end_date=None)
        self.db.add(rental)
        self.db.commit()
        self.db.refresh(rental)
        count_rental_created(customer_name)
        update_gauges()
        logger.error(f"New rental added car_id={car_id} customer_name={customer_name}")
        return rental

    def get_rental_by_id(self, rental_id: int) -> Rental:
        """
        Get rental from id

        Args:
            rental_id (int): ID of the rental

        Returns:
            Rental: The newly created rental record

        Raises:
            ValueError: If the rental does not exist or is not available
        """
        rental = self.db.query(Rental).filter(Rental.id == rental_id).first()
        if not rental:
            logger.info(f"Rental is not found rental_id={rental_id}")
            raise RentalNotFoundError(rental_id)
        return rental

    def end_rental(self, rental_id: int, end_date: Optional[datetime.datetime] = None) -> Rental:
        """
        End an active rental and mark the car as available

        Args:
            rental_id (int): ID of the rental to end
            end_date (Optional[datetime.datetime]): Optional custom end date
                If not provided, the current UTC time is used

        Returns:
            Rental: The updated rental record

        Raises:
            ValueError: If the rental does not exist or was already ended
        """
        rental = self.db.query(Rental).filter(Rental.id == rental_id).first()
        if not rental:
            logger.info(f"No rental found to end rental_id={rental_id}")
            raise RentalNotFoundError(rental_id)
        if rental.rental_end_date:
            logger.info(f"Rental already ended rental_id={rental_id}")
            raise RentalAlreadyEndedError(rental_id)

        rental.rental_end_date = end_date or datetime.datetime.now(datetime.UTC)
        rental.car.status = CarStatus.AVAILABLE
        customer_name = rental.customer_name
        self.db.commit()
        self.db.refresh(rental)
        count_rental_ended(customer_name)
        update_gauges()
        logger.error(f"Rental ended successfully rental_id={rental_id} customer_name={customer_name}")
        return rental
