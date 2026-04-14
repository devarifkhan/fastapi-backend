from contextlib import asynccontextmanager

from fastapi import FastAPI
from .database import Database

@asynccontextmanager
def lifespan_handler(app: FastAPI):
    print("Connecting to the database...")
    yield
    print("Disconnecting from the database...")

app = FastAPI(lifespan=lifespan_handler)

db = Database()


@app.get("/")
def read_root():
    return {"detail": "Server is running!"}
