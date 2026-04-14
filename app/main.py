from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference
from typing import Any
from .schemas import ShipmentCreate, ShipmentRead, ShipmentUpdate, ShipmentStatus
from .database import Database
from contextlib import asynccontextmanager


@asynccontextmanager
def lifespan_handler(app: FastAPI):
    print("Connecting to the database...")
    yield
    print("Disconnecting from the database...")

app = FastAPI(lifespan=lifespan_handler)

db = Database()


@app.get("/shipment")
def get_shipment(id: int | None = None, shipment_status: ShipmentStatus | None = None) -> Any:
    if shipment_status is not None:
        return {k: v for k, v in shipments.items() if v["status"] == shipment_status}

    if id is None:
        id = max(shipments.keys())

    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found"
        )
    return shipments[id]


@app.post("/shipment", status_code=status.HTTP_201_CREATED)
def submit_shipment(shipment: ShipmentCreate) -> dict[str, int]:
    new_id = max(shipments.keys()) + 1
    shipments[new_id] = {
        **shipment.model_dump(),
        "id": new_id,
        "status": ShipmentStatus.placed,
    }
    save()
    return {"id": new_id}


@app.get("/shipment/{field}")
def get_shipment_field(field: str, id: int) -> dict[str, Any]:
    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found"
        )
    if field not in shipments[id]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Field not found"
        )
    return {field: shipments[id][field]}


@app.put("/shipment", response_model=ShipmentRead)
def shipment_update(id: int, shipment: ShipmentRead) -> dict[str, Any]:
    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found"
        )
    shipments[id] = shipment.model_dump()
    return shipments[id]


@app.patch("/shipment/{id}/status", response_model=ShipmentRead)
def update_shipment_status(id: int, shipment_status: ShipmentStatus) -> dict[str, Any]:
    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found"
        )
    shipments[id]["status"] = shipment_status
    save()
    return shipments[id]


@app.patch("/shipment", response_model=ShipmentRead)
def update_shipment(id: int, body: ShipmentUpdate) -> dict[str, Any]:
    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found"
        )
    shipments[id].update(body.model_dump(exclude_none=True))
    return shipments[id]


@app.delete("/shipment")
def delete_shipment(id: int) -> dict[str, str]:
    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found"
        )
    del shipments[id]
    return {"detail": f"Shipment with ID {id} deleted successfully"}


@app.get("/scaler", include_in_schema=False)
def get_scaler_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scaler API",
    )
