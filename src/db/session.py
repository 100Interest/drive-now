import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.db.models import DeclarativeBase

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///.test.db")
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    FastAPI dependency that provides a database session.

    Yields:
        Session: An active SQLAlchemy session for the duration of the request.

    The session is automatically closed after the request is finished,
    even if an exception occurs.
    """
    db = Session()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    DeclarativeBase.metadata.create_all(bind=engine)
