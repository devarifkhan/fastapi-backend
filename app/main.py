from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference
from typing import Any
from datetime import datetime, timedelta

from sqlmodel import select
from .schemas import ShipmentCreate, ShipmentRead, ShipmentUpdate, ShipmentStatus
from .database.models import Shipment
from contextlib import asynccontextmanager
from .database.session import create_db_and_tables, sessionDep


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan_handler)


@app.get("/shipment", response_model=ShipmentRead)
def get_shipment(session: sessionDep, id: int | None = None, shipment_status: ShipmentStatus | None = None) -> Any:
    if id is not None:
        shipment = session.get(Shipment, id)
        if shipment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found")
        return shipment

    query = select(Shipment)
    if shipment_status is not None:
        query = query.where(Shipment.status == shipment_status)
    return session.exec(query).all()


@app.post("/shipment", status_code=status.HTTP_201_CREATED)
def submit_shipment(shipment: ShipmentCreate, session: sessionDep) -> dict[str, int]:
    new_shipment = Shipment(
        **shipment.model_dump(),
        status=ShipmentStatus.placed,
        estimated_delivery=datetime.now() + timedelta(days=7),
    )
    session.add(new_shipment)
    session.commit()
    session.refresh(new_shipment)
    return {"id": new_shipment.id}


@app.get("/shipment/{field}")
def get_shipment_field(field: str, id: int, session: sessionDep) -> dict[str, Any]:
    shipment = session.get(Shipment, id)
    if shipment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found")
    shipment_dict = shipment.model_dump()
    if field not in shipment_dict:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Field not found")
    return {field: shipment_dict[field]}


@app.put("/shipment", response_model=ShipmentRead)
def shipment_update(id: int, shipment: ShipmentRead, session: sessionDep) -> Any:
    db_shipment = session.get(Shipment, id)
    if db_shipment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found")
    for key, value in shipment.model_dump().items():
        setattr(db_shipment, key, value)
    session.add(db_shipment)
    session.commit()
    session.refresh(db_shipment)
    return db_shipment


@app.patch("/shipment/{id}/status", response_model=ShipmentRead)
def update_shipment_status(id: int, shipment_status: ShipmentStatus, session: sessionDep) -> Any:
    shipment = session.get(Shipment, id)
    if shipment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found")
    shipment.status = shipment_status
    session.add(shipment)
    session.commit()
    session.refresh(shipment)
    return shipment


@app.patch("/shipment", response_model=ShipmentRead)
def update_shipment(id: int, body: ShipmentUpdate, session: sessionDep) -> Any:
    shipment = session.get(Shipment, id)
    if shipment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found")
    for key, value in body.model_dump(exclude_none=True).items():
        setattr(shipment, key, value)
    session.add(shipment)
    session.commit()
    session.refresh(shipment)
    return shipment


@app.delete("/shipment")
def delete_shipment(id: int, session: sessionDep) -> dict[str, str]:
    shipment = session.get(Shipment, id)
    if shipment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found")
    session.delete(shipment)
    session.commit()
    return {"detail": f"Shipment with ID {id} deleted successfully"}


@app.get("/scaler", include_in_schema=False)
def get_scaler_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scaler API",
    )
