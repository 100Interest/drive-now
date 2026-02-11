from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.router.car import car_router
from src.api.router.rental import rental_router
from src.db.session import create_tables
from src.metrics import mount_metrics, update_gauges


@asynccontextmanager
async def lifespan(app: FastAPI):
    """ lifespan events """
    create_tables()
    update_gauges()
    yield


app = FastAPI(title="DriveNow", lifespan=lifespan)
app.include_router(car_router)
app.include_router(rental_router)
mount_metrics(app)
