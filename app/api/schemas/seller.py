from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class SellerCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    address: str
    zip_code: int


class SellerLogin(BaseModel):
    email: EmailStr
    password: str


class SellerUpdate(BaseModel):
    name: str | None = None
    address: str | None = None
    zip_code: int | None = None
    password: str | None = None


class SellerRead(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    address: str
    zip_code: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class LoginResponse(BaseModel):
    seller_id: UUID
    name: str


class SellerStats(BaseModel):
    total: int
    placed: int
    in_transit: int
    out_for_delivery: int
    delivered: int
    cancelled: int
