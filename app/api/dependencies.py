from typing import Annotated
from uuid import UUID

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_session
from app.services.shipment import ShipmentService
from app.services.seller import SellerService


# Asynchronous database session dep annotation
SessionDep = Annotated[AsyncSession, Depends(get_session)]


# Shipment service dep
def get_shipment_service(session: SessionDep) -> ShipmentService:
    return ShipmentService(session)


# Shipment service dep annotation
ServiceDep = Annotated[ShipmentService, Depends(get_shipment_service)]
ShipmentServiceDep = ServiceDep


# Seller service dep
def get_seller_service(session: SessionDep) -> SellerService:
    return SellerService(session)


SellerServiceDep = Annotated[SellerService, Depends(get_seller_service)]


# Current seller dep — pass UUID via X-Seller-Id header
async def get_current_seller(
    session: SessionDep,
    x_seller_id: Annotated[UUID | None, Header()] = None,
):
    from app.database.models import Seller

    if x_seller_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="X-Seller-Id header is required",
        )
    seller = await session.get(Seller, x_seller_id)
    if seller is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Seller not found",
        )
    return seller


SellerDep = Annotated[object, Depends(get_current_seller)]


# Current delivery partner dep — pass UUID via X-Partner-Id header
async def get_current_partner(
    session: SessionDep,
    x_partner_id: Annotated[UUID | None, Header()] = None,
):
    from app.database.models import DeliveryPartner

    if x_partner_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="X-Partner-Id header is required",
        )
    partner = await session.get(DeliveryPartner, x_partner_id)
    if partner is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Delivery partner not found",
        )
    return partner


DeliveryPartnerDep = Annotated[object, Depends(get_current_partner)]
