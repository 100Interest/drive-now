from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel

from src.db.models import CarStatus
from src.db.session import Session, get_db
from src.services.car import CarService


class CarCreate(BaseModel):
    model: str
    year: int


car_router = APIRouter(prefix="/car", tags=["Car"])


@car_router.post("/")
def create_car(car: CarCreate, db: Session = Depends(get_db)):
    service = CarService(db)
    return service.add_car(model=car.model, year=car.year)


@car_router.get("/")
def list_all_cars(status: str = None, limit: int = Query(default=5, ge=1, le=100), db: Session = Depends(get_db)):
    service = CarService(db)
    car_status = CarStatus(status) if status else None
    return service.list_cars(status=car_status, limit=limit)


@car_router.get("/{car_id}")
def get_car_by_id(car_id: int, db: Session = Depends(get_db)):
    service = CarService(db)
    return service.get_car_by_id(car_id)
