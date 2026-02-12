import datetime

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from src.db.session import Session, get_db
from src.services.rental import RentalService


class CreateRentalPayload(BaseModel):
    """
        Request schema for creating a rental
    """
    car_id: int
    customer_name: str


class EndRentalPayload(BaseModel):
    """
        Request schema for ending a rental.
    """
    end_date: datetime.datetime = None


rental_router = APIRouter(prefix="/rental", tags=["Rental"])


@rental_router.post("/")
def create_rental(rental_payload: CreateRentalPayload, db: Session = Depends(get_db)):
    """
       Create a new rental for a specific car

       Args:
           car_id (int): ID of the car to rent
           customer_name (str): Name of the customer
           db (Session): Database session dependency

       Returns:
           Rental: The newly created rental

       Raises:
           ValueError: If the car is not available
    """
    service = RentalService(db)
    return service.create_new_rental(rental_payload.car_id, rental_payload.customer_name)


@rental_router.post("/{rental_id}/end")
def end_rental(rental_id: int, end_rental_payload: EndRentalPayload = None, db: Session = Depends(get_db)):
    """
       End an active rental

       Args:
           rental_id (int): ID of the rental to end
           end_rental_payload (EndRentalPayload | None): Optional payload
               containing a custom end date
           db (Session): Database session dependency

       Returns:
           Rental: The updated rental record
    """
    service = RentalService(db)
    end_date = end_rental_payload.end_date if end_rental_payload.end_date else None
    rental = service.end_rental(rental_id, end_date)
    return rental


@rental_router.get("/")
def get_rental_by_id(rental_id: int, db: Session = Depends(get_db)):
    """
       Get rental by its ID

       Args:
           rental_id (int): ID of the rental

       Returns:
           Rental: The rental if found
    """
    service = RentalService(db)
    rental = service.get_rental_by_id(rental_id)
    return rental
