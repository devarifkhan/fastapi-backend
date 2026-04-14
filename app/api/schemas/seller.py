from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class SellerCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    address: str
    zip_code: int


class SellerRead(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    address: str
    zip_code: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
