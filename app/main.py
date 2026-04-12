from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference
from typing import Any

app = FastAPI()


@app.get("/shipment/latest")
def get_latest_shipment() -> dict[str, Any]:
    return {
        "id": 123,
        "content": "wooden chair",
        "weight": 15.0,
        "status": "placed",
    }


@app.get("/shipment/{id}")
def get_shipment(id:int) -> dict[str, Any]:
    return {
        "id": id,
        "content": "wooden table",
        "weight": 20.5,
        "status": "in transit",
    }



@app.get("/scaler",include_in_schema=False)
def get_scaler_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scaler API",
    )