from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference
from typing import Any
from pydantic import BaseModel


class Shipment(BaseModel):
    content: str
    weight: float
    destination: str


app = FastAPI()

shipments = {
    12701: {"weight": 15.0, "content": "wooden chair", "status": "placed"},
    12702: {"weight": 24.0, "content": "office desk", "status": "in transit"},
    12703: {"weight": 8.2, "content": "floor lamp", "status": "delivered"},
    12704: {"weight": 3.5, "content": "wall mirror", "status": "placed"},
    12705: {"weight": 40.0, "content": "dining table", "status": "in transit"},
    12706: {"weight": 12.7, "content": "bookshelf", "status": "delivered"},
    12707: {"weight": 5.0, "content": "ceiling fan", "status": "placed"},
    12708: {"weight": 18.3, "content": "coffee table", "status": "in transit"},
    12709: {"weight": 2.1, "content": "table clock", "status": "delivered"},
    12710: {"weight": 28.9, "content": "bed frame", "status": "placed"},
    12711: {"weight": 9.4, "content": "office chair", "status": "in transit"},
}


@app.get("/shipment")
def get_shipment(id: int | None = None) -> dict[str, Any]:

    if id is None:
        id = max(shipments.keys())
        return shipments[id]

    if not id in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found"
        )
    return shipments[id]


@app.post("/shipment")
def submit_shipment(shipment: Shipment) -> dict[str, Any]:

    if shipment.weight > 25:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Shipment weight exceeds the limit of 25 kg",
        )

    new_id = max(shipments.keys()) + 1
    shipments[new_id] = {
        "weight": shipment.weight,
        "content": shipment.content,
        "status": "placed",
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


@app.put("/shipment")
def shipment_update(id: int, shipment: Shipment) -> dict[str, Any]:
    shipments[id] = {
        "weight": shipment.weight,
        "content": shipment.content,
        "status": shipment.status,
    }
    return shipments[id]


@app.patch("/shipment")
def patch_shipment(id: int, shipment: Shipment) -> dict[str, Any]:
    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found"
        )
    if shipment.content is not None:
        shipments[id]["content"] = shipment.content
    if shipment.weight is not None:
        shipments[id]["weight"] = shipment.weight
    if shipment.status is not None:
        shipments[id]["status"] = shipment.status
    return shipments[id]


@app.delete("/shipment")
def delete_shipment(id: int) -> dict[str, Any]:
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
