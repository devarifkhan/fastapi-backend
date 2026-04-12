from pydantic import BaseModel,Field

class Shipment(BaseModel):
    content: str
    weight: float = Field(le=25)
    destination: str