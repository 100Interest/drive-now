import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import DeclarativeBase

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///.test.db")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    DeclarativeBase.metadata.create_all(bind=engine)
