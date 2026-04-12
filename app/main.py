from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

app = FastAPI()


@app.get("/shipment")
def get_shipment():
    return {
        "content": "wooden table",
        "status": "in transit",
    }

@app.get("/scaler")
def get_scaler_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scaler API",
    )