from pydantic import BaseModel,Field
from random import randint


def random_destination() -> int:
    return randint(11000, 11999)

class Shipment(BaseModel):
    content: str = Field(max_length=30)
    weight: float = Field(le=25,ge=1)
    destination: int | None = Field(default_factory=random_destination)