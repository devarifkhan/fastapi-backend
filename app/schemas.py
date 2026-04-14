from enum import Enum
from pydantic import BaseModel, Field
from random import randint
from .database.models import ShipmentStatus

def random_destination() -> int:
    return randint(11000, 11999)




class BaseShipment(BaseModel):
    content: str = Field(max_length=30)
    weight: float = Field(le=25, ge=1)
    destination: int | None = Field(default_factory=random_destination)


class ShipmentRead(BaseShipment):
    status: ShipmentStatus = ShipmentStatus.placed


class Order(BaseModel):
    price: int
    description: str
    title: str


class ShipmentCreate(BaseShipment):
    pass


class ShipmentUpdate(BaseModel):
    content: str | None = Field(default=None, max_length=30)
    weight: float | None = Field(default=None, le=25, ge=1)
    destination: int | None = Field(default=None)
    status: ShipmentStatus | None = Field(default=None)
