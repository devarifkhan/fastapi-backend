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

class BaseShipment(BaseModel):
    content: str = Field(max_length=30)
    weight: float = Field(le=25, ge=1)
    destination: int | None = Field(default_factory=random_destination)


class ShipmentRead(BaseShipment):
    content: str = Field(max_length=30)
    weight: float = Field(le=25, ge=1)
    destination: int | None = Field(default_factory=random_destination)
    status: ShipmentStatus = ShipmentStatus.placed

class ShipmentCreate(BaseShipment):
    content: str = Field(max_length=30)
    weight: float = Field(le=25, ge=1)
    destination: int | None = Field(default_factory=random_destination) 

class ShipmentUpdate(BaseModel):
    content: str | None = Field(default=None, max_length=30)
    weight: float | None = Field(default=None, le=25, ge=1)
    destination: int | None = Field(default=None)
    status: ShipmentStatus | None = Field(default=None)