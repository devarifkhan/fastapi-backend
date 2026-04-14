from datetime import datetime
from enum import Enum

from sqlmodel import SQLModel, Field


class ShipmentStatus(str, Enum):
    placed = "placed"
    in_transit = "in transit"
    delivered = "delivered"
    out_for_delivery = "out for delivery"


class Shipment(SQLModel, table=True):

    __tablename__ = "shipment"

    id: int | None = Field(default=None, primary_key=True)
    content: str
    weight: float = Field(le=25)
    destination: int
    status: ShipmentStatus
    estimated_delivery: datetime