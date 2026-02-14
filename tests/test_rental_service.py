import pytest
from unittest.mock import patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.db.models import DeclarativeBase, CarStatus
from src.services.car import CarService
from src.services.rental import RentalService
from src.exceptions import CarUnavailableError


@pytest.fixture(scope="function")
def db_session():
    """ Create clean in-memory DB session """
    engine = create_engine("sqlite:///:memory:")
    DeclarativeBase.metadata.create_all(bind=engine)

    local_db_session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    db = local_db_session()

    try:
        yield db
    finally:
        db.rollback()
        db.close()
        DeclarativeBase.metadata.drop_all(bind=engine)


@patch("src.services.rental.update_gauges")
@patch("src.services.rental.count_rental_created")
def test_create_new_rental_success(mock_count, mock_update, db_session):
    """ Create rental and verify car status and rental fields """
    car_service = CarService(db_session)
    rental_service = RentalService(db_session)

    car = car_service.add_car("Toyota", 2020)

    rental = rental_service.create_new_rental(car.id, "Daniel")

    assert rental.car_id == car.id
    assert rental.customer_name == "Daniel"
    assert rental.rental_end_date is None

    # Verify car status changed in DB
    updated_car = car_service.get_car_by_id(car.id)
    assert updated_car.status == CarStatus.IN_USE


def test_create_new_rental_car_unavailable(db_session):
    """ Creating rental for IN_USE car should raise error """
    car_service = CarService(db_session)
    rental_service = RentalService(db_session)

    car = car_service.add_car("BMW", 2022)
    car_service.update_car_status_by_car_id(car.id, CarStatus.IN_USE)

    with pytest.raises(CarUnavailableError):
        rental_service.create_new_rental(car.id, "David")


@patch("src.services.rental.update_gauges")
@patch("src.services.rental.count_rental_created")
def test_end_rental_success(mock_count, mock_update, db_session):
    """ End rental and verify car becomes AVAILABLE """
    car_service = CarService(db_session)
    rental_service = RentalService(db_session)

    car = car_service.add_car("Honda", 2018)
    rental = rental_service.create_new_rental(car.id, "Noa")

    ended_rental = rental_service.end_rental(rental.id)

    assert ended_rental.rental_end_date is not None

    # Verify car status returned to AVAILABLE
    updated_car = car_service.get_car_by_id(car.id)
    assert updated_car.status == CarStatus.AVAILABLE
