from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel

from src.db.models import CarStatus
from src.db.session import Session, get_db
from src.services.car import CarService


class CarCreate(BaseModel):
    model: str
    year: int


class CarStatusUpdate(BaseModel):
    status: CarStatus


car_router = APIRouter(prefix="/car", tags=["Car"])


@car_router.post("/")
def create_car(car: CarCreate, db: Session = Depends(get_db)):
    service = CarService(db)
    return service.add_car(car.model, car.year)


@car_router.get("/")
def list_all_cars(status: str = None, limit: int = Query(default=5, ge=1, le=100), db: Session = Depends(get_db)):
    service = CarService(db)
    car_status = CarStatus(status) if status else None
    return service.list_cars(car_status, limit)


@car_router.get("/{car_id}")
def get_car_by_id(car_id: int, db: Session = Depends(get_db)):
    service = CarService(db)
    return service.get_car_by_id(car_id)


@car_router.patch("/{car_id}")
def update_car_status(car_id: int, new_status_payload: CarStatusUpdate, db: Session = Depends(get_db)):
    service = CarService(db)
    new_status = new_status_payload.status
    return service.update_car_status_by_car_id(car_id, new_status)
