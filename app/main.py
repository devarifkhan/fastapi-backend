from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference
from typing import Any
from .schemas import ShipmentCreate, ShipmentRead, ShipmentUpdate, ShipmentStatus


app = FastAPI()

shipments: dict[int, dict] = {
    12701: {"weight": 15.0, "content": "wooden chair", "status": "placed", "destination": 11201},
    12702: {"weight": 24.0, "content": "office desk", "status": "in transit", "destination": 11345},
    12703: {"weight": 8.2, "content": "floor lamp", "status": "delivered", "destination": 11567},
    12704: {"weight": 3.5, "content": "wall mirror", "status": "placed", "destination": 11890},
    12705: {"weight": 20.0, "content": "dining table", "status": "in transit", "destination": 11123},
    12706: {"weight": 12.7, "content": "bookshelf", "status": "delivered", "destination": 11456},
    12707: {"weight": 5.0, "content": "ceiling fan", "status": "placed", "destination": 11789},
    12708: {"weight": 18.3, "content": "coffee table", "status": "in transit", "destination": 11234},
    12709: {"weight": 2.1, "content": "table clock", "status": "delivered", "destination": 11678},
    12710: {"weight": 24.9, "content": "bed frame", "status": "placed", "destination": 11901},
    12711: {"weight": 9.4, "content": "office chair", "status": "in transit", "destination": 11543},
}


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
        "status": ShipmentStatus.placed,
    }
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
