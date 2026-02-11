from fastapi import FastAPI

from src.api.router.car import car_router
from src.db.session import create_tables

create_tables()

app = FastAPI(title="DriveNow")
app.include_router(car_router)
