from fastapi import HTTPException, status


class CarNotFoundError(HTTPException):
    """ This error is being raised when the car is not found yet the user tries to fetch/rent it """

    def __init__(self, car_id: int):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND,
                         detail=f"Car with id {car_id} not found")


class CarUnavailableError(HTTPException):
    """ This error is being raised when the car is not available yet the user tries to rent it """

    def __init__(self, car_id: int, car_status: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST,
                         detail=f"Car with id {car_id} is not available, current status: {car_status}")


class RentalNotFoundError(HTTPException):
    """ This error is being raised when the user tries to end a non-existent rental """

    def __init__(self, rental_id: int):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND,
                         detail=f"Rental with id {rental_id} not found")


class RentalAlreadyEndedError(HTTPException):
    """ This error is being raised when the user tries to end an already ended rental """

    def __init__(self, rental_id: int):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST,
                         detail=f"Rental with id {rental_id} already ended")
