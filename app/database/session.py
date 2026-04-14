from sqlmodel import SQLModel, Session, create_engine
from .models import Shipment  # noqa: F401 — ensures table is registered

engine = create_engine(
    url="sqlite:///sqlite.db",
    echo=True,
    connect_args={"check_same_thread": False},
)


class Database:
    def __init__(self):
        SQLModel.metadata.create_all(bind=engine)

    def get_session(self):
        return Session(engine)
