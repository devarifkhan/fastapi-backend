from enum import Enum
from pydantic import BaseModel, Field
from random import randint


def random_destination() -> int:
    return randint(11000, 11999)


class ShipmentStatus(str, Enum):
    placed = "placed"
    in_transit = "in transit"
    delivered = "delivered"
    out_for_delivery = "out for delivery"


class Shipment(BaseModel):
    content: str = Field(max_length=30)
    weight: float = Field(le=25, ge=1)
    destination: int | None = Field(default_factory=random_destination)
    status: ShipmentStatus = ShipmentStatus.placed