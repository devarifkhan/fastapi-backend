from datetime import datetime, timedelta
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.api.schemas.shipment import ShipmentCreate, ShipmentUpdate
from app.database.models import (
    DeliveryPartner,
    Review,
    Seller,
    ServicableLocation,
    Shipment,
    ShipmentEvent,
    ShipmentStatus,
    TagName,
)


class ShipmentService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: UUID) -> Shipment:
        result = await self.session.execute(
            select(Shipment).where(Shipment.id == id)
        )
        shipment = result.scalar_one_or_none()
        if shipment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Shipment not found",
            )
        return shipment

    async def add(self, shipment_create: ShipmentCreate, seller: Seller) -> Shipment:
        partner = await self._find_partner(shipment_create.destination)

        new_shipment = Shipment(
            **shipment_create.model_dump(),
            seller_id=seller.id,
            delivery_partner_id=partner.id,
            estimated_delivery=datetime.now() + timedelta(days=3),
        )
        self.session.add(new_shipment)
        await self.session.flush()

        # Initial timeline event
        event = ShipmentEvent(
            shipment_id=new_shipment.id,
            status=ShipmentStatus.placed,
            location=shipment_create.destination,
            description="Shipment placed",
        )
        self.session.add(event)
        await self.session.commit()
        await self.session.refresh(new_shipment)
        return new_shipment

    async def update(
        self,
        id: UUID,
        shipment_update: ShipmentUpdate,
        partner: DeliveryPartner,
    ) -> Shipment:
        shipment = await self.get(id)

        if shipment_update.status is not None:
            event = ShipmentEvent(
                shipment_id=shipment.id,
                status=shipment_update.status,
                location=shipment.destination,
            )
            self.session.add(event)

        if shipment_update.estimated_delivery is not None:
            shipment.estimated_delivery = shipment_update.estimated_delivery
            self.session.add(shipment)

        await self.session.commit()
        await self.session.refresh(shipment)
        return shipment

    async def cancel(self, id: UUID, seller: Seller) -> None:
        shipment = await self.get(id)

        if shipment.seller_id != seller.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to cancel this shipment",
            )

        event = ShipmentEvent(
            shipment_id=shipment.id,
            status=ShipmentStatus.cancelled,
            location=shipment.destination,
            description="Cancelled by seller",
        )
        self.session.add(event)
        await self.session.commit()

    async def add_tag(self, id: UUID, tag_name: TagName) -> Shipment:
        shipment = await self.get(id)
        tag = await tag_name.tag(self.session)

        if tag is not None and tag not in shipment.tags:
            shipment.tags.append(tag)
            self.session.add(shipment)
            await self.session.commit()
            await self.session.refresh(shipment)

        return shipment

    async def remove_tag(self, id: UUID, tag_name: TagName) -> Shipment:
        shipment = await self.get(id)
        tag = await tag_name.tag(self.session)

        if tag is not None and tag in shipment.tags:
            shipment.tags.remove(tag)
            self.session.add(shipment)
            await self.session.commit()
            await self.session.refresh(shipment)

        return shipment

    async def rate(self, token: str, rating: int, comment: str | None) -> None:
        shipment_id = UUID(token)
        shipment = await self.get(shipment_id)

        review = Review(
            shipment_id=shipment.id,
            rating=rating,
            comment=comment,
        )
        self.session.add(review)
        await self.session.commit()

    async def _find_partner(self, zip_code: int) -> DeliveryPartner:
        result = await self.session.execute(
            select(DeliveryPartner)
            .join(
                ServicableLocation,
                ServicableLocation.partner_id == DeliveryPartner.id,
            )
            .where(ServicableLocation.location_id == zip_code)
            .limit(1)
        )
        partner = result.scalars().first()
        if partner is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No delivery partner available for this destination",
            )
        return partner
