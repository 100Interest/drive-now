import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from src.db.session import Session, get_db
from src.services.rental import RentalService


class EndRentalPayload(BaseModel):
    """
        Request schema for ending a rental.
    """
    end_date: datetime.datetime = None


rental_router = APIRouter(prefix="/rental", tags=["Rental"])


@rental_router.post("/")
def create_rental(car_id: int, customer_name: str, db: Session = Depends(get_db)):
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
    return service.create_new_rental(car_id, customer_name)


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

       Raises:
           HTTPException: If the rental does not exist or was already ended
    """
    service = RentalService(db)
    end_date = end_rental_payload.end_date if end_rental_payload.end_date else None
    try:
        rental = service.end_rental(rental_id, end_date)
        return rental
    except ValueError as err:
        raise HTTPException(status_code=404, detail=f"Rental id {rental_id} was not found\n{err}")
