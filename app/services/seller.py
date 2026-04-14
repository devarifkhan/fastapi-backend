import hashlib
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.api.schemas.seller import SellerCreate, SellerUpdate
from app.database.models import Seller


class SellerService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: UUID) -> Seller:
        result = await self.session.execute(select(Seller).where(Seller.id == id))
        seller = result.scalar_one_or_none()
        if seller is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Seller not found")
        return seller

    async def add_seller(self, seller_create: SellerCreate) -> Seller:
        # Check email not already taken
        existing = await self.session.execute(select(Seller).where(Seller.email == seller_create.email))
        if existing.scalar_one_or_none() is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

        password_hash = hashlib.sha256(seller_create.password.encode()).hexdigest()
        seller = Seller(
            name=seller_create.name,
            email=seller_create.email,
            password_hash=password_hash,
            address=seller_create.address,
            zip_code=seller_create.zip_code,
        )
        self.session.add(seller)
        await self.session.commit()
        await self.session.refresh(seller)
        return seller

    async def login(self, email: str, password: str) -> Seller:
        result = await self.session.execute(select(Seller).where(Seller.email == email))
        seller = result.scalar_one_or_none()
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        if seller is None or seller.password_hash != password_hash:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )
        return seller

    async def update(self, seller: Seller, data: SellerUpdate) -> Seller:
        update_dict = data.model_dump(exclude_none=True)
        if "password" in update_dict:
            update_dict["password_hash"] = hashlib.sha256(
                update_dict.pop("password").encode()
            ).hexdigest()
        seller.sqlmodel_update(update_dict)
        self.session.add(seller)
        await self.session.commit()
        await self.session.refresh(seller)
        return seller

    async def delete(self, seller: Seller) -> None:
        await self.session.delete(seller)
        await self.session.commit()
