from fastapi import FastAPI
from src.db.session import create_tables

create_tables()

app = FastAPI(title="DriveNow")
