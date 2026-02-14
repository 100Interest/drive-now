import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.db.models import DeclarativeBase, CarStatus
from src.services.car import CarService

LOCAL_SQL_MOCK_URL = "sqlite:///./car_service_mock.db"


@pytest.fixture(scope="session")
def engine():
    """ Create an SQLAlchemy engine """
    engine = create_engine(LOCAL_SQL_MOCK_URL)
    DeclarativeBase.metadata.create_all(bind=engine)
    yield engine
    DeclarativeBase.metadata.drop_all(bind=engine)


@pytest.fixture(scope="session")
def db_session(engine):
    """ create a database """
    test_session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    db = test_session()
    try:
        yield db
    finally:
        db.close()


def test_add_car(db_session):
    """ Create a car, add it and validate its attributes """
    service = CarService(db_session)
    car = service.add_car("Mazda", 2013)
    assert car.model == "Mazda"
    assert car.year == 2013
    assert car.status == CarStatus.AVAILABLE


def test_update_car_status(db_session):
    """ Create a car, change its status and check the updated status is under maintenance """
    service = CarService(db_session)
    car = service.add_car("Ferrari", 2021)

    # Verify the output of the service
    updated_car = service.update_car_status_by_car_id(car.id, CarStatus.UNDER_MAINTENANCE)
    assert updated_car.status == CarStatus.UNDER_MAINTENANCE

    # Verify this also in the DB itself
    updated_car_in_db = service.get_car_by_id(car.id)
    assert updated_car_in_db.status == CarStatus.UNDER_MAINTENANCE


def test_list_cars(db_session):
    """ Add 2 cars and check the length of the list cars output, check the specific number of IN_USE cars too """
    service = CarService(db_session)
    service.add_car("Rimac", 2021)
    service.add_car("Aston Martin", 2021)
    service.update_car_status_by_car_id(2, CarStatus.IN_USE)

    # Verify 2 total cars were added
    all_cars = service.list_cars()
    assert len(all_cars) == 2

    # The number of IN_USE cars is 1 as only the Aston Martin was changed from AVAILABLE to IN_USE
    all_in_use_cars = service.list_cars(CarStatus.IN_USE)
    assert len(all_in_use_cars) == 1
