from typing import Annotated

from fastapi import Depends
from sqlmodel import SQLModel, Session, create_engine
from .models import Shipment

engine = create_engine(
    url="sqlite:///sqlite.db",
    echo=True,
    connect_args={"check_same_thread": False},
)


def create_db_and_tables():
 
    SQLModel.metadata.create_all(bind=engine) 


def get_session():
    with Session(engine) as session:
        yield session

sessionDep = Annotated[Session, Depends(get_session)]