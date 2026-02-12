import logging

from prometheus_client import (Counter, Gauge, Histogram,
                               start_http_server, make_asgi_app)

from src.db.models import Car, Rental, CarStatus
from src.db.session import Session as LocalSession

logger = logging.getLogger(__name__)

# Counters
CARS_ADDED = Counter("total_cars_added", "Total cars added", ["model"])
RENTALS_CREATED = Counter("total_rentals_created", "Total rentals created", ["customer_name"])
RENTALS_ENDED = Counter("total_rentals_ended", "Total rentals completed", ["customer_name"])

# Gauges
AVAILABLE_CARS = Gauge("total_available_cars", "Number of AVAILABLE cars")
ONGOING_RENTALS = Gauge("total_ongoing_rentals", "Number of active rentals")

# Histograms
REQUEST_TIME = Histogram("http_request_time_seconds",
                         "HTTP request duration",
                         ["method", "endpoint"])


def start_metrics_server(port=7779):
    """ HTTP server for metrics """
    start_http_server(port)
    logger.info(f"Local Prometheus metrics server started on: http://localhost:{port}/metrics")


def mount_metrics(app):
    """ Mount the metrics server to the main application """
    app.mount("/metrics", make_asgi_app())


def update_gauges():
    """ Update ongoing events (gauges) """
    with LocalSession() as session:
        # Count AVAILABLE cars
        active_cars = session.query(Car).filter(Car.status == CarStatus.AVAILABLE).count()
        AVAILABLE_CARS.set(active_cars)

        # Count rentals WHERE end_date IS NULL (yet to terminate)
        ongoing_rentals = session.query(Rental).filter(Rental.rental_end_date.is_(None)).count()
        ONGOING_RENTALS.set(ongoing_rentals)


def count_car_added(model: str):
    CARS_ADDED.labels(model=model).inc()


def count_rental_created(customer_name: str):
    RENTALS_CREATED.labels(customer_name=customer_name).inc()


def count_rental_ended(customer_name: str):
    RENTALS_ENDED.labels(customer_name=customer_name).inc()
