import hashlib

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.seller import SellerCreate
from app.database.models import Seller


class SellerService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_seller(self, seller_create: SellerCreate) -> Seller:
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
