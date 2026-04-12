from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference
from typing import Any

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


@app.get("/shipment/latest")
def get_latest_shipment() -> dict[str, Any]:
    id = max(shipments.keys())
    return shipments[id]


@app.get("/shipment/{id}")
def get_shipment(id: int) -> dict[str, Any]:
    return shipments[id]


@app.get("/scaler", include_in_schema=False)
def get_scaler_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scaler API",
    )
