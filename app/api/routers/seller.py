from fastapi import APIRouter

from app.api.tag import APITag
from app.api.schemas.seller import (
    LoginResponse,
    SellerCreate,
    SellerLogin,
    SellerRead,
    SellerStats,
    SellerUpdate,
)
from app.api.schemas.shipment import ShipmentRead
from app.database.models import ShipmentStatus
from ..dependencies import SellerDep, SellerServiceDep

router = APIRouter(prefix="/seller", tags=[APITag.SELLER])


### Register a new seller
@router.post("/signup", response_model=SellerRead, status_code=201)
async def register_seller(
    seller: SellerCreate,
    service: SellerServiceDep,
):
    return await service.add_seller(seller)


### Login — returns seller_id to use as X-Seller-Id header
@router.post("/login", response_model=LoginResponse)
async def login(
    credentials: SellerLogin,
    service: SellerServiceDep,
):
    seller = await service.login(credentials.email, credentials.password)
    return LoginResponse(seller_id=seller.id, name=seller.name)


### Get own profile
@router.get("/me", response_model=SellerRead)
async def get_me(seller: SellerDep):
    return seller


### Update own profile
@router.patch("/me", response_model=SellerRead)
async def update_me(
    update: SellerUpdate,
    seller: SellerDep,
    service: SellerServiceDep,
):
    return await service.update(seller, update)


### Delete own account
@router.delete("/me", status_code=204)
async def delete_me(
    seller: SellerDep,
    service: SellerServiceDep,
):
    await service.delete(seller)


### Get all shipments
@router.get("/shipments", response_model=list[ShipmentRead])
async def get_shipments(seller: SellerDep):
    return seller.shipments


### Get only active shipments (placed / in-transit / out for delivery)
@router.get("/shipments/active", response_model=list[ShipmentRead])
async def get_active_shipments(seller: SellerDep):
    terminal = {ShipmentStatus.delivered, ShipmentStatus.cancelled}
    return [s for s in seller.shipments if s.status not in terminal]


### Shipment statistics
@router.get("/stats", response_model=SellerStats)
async def get_stats(seller: SellerDep):
    shipments = seller.shipments
    statuses = [s.status for s in shipments]
    return SellerStats(
        total=len(shipments),
        placed=statuses.count(ShipmentStatus.placed),
        in_transit=statuses.count(ShipmentStatus.in_transit),
        out_for_delivery=statuses.count(ShipmentStatus.out_for_delivery),
        delivered=statuses.count(ShipmentStatus.delivered),
        cancelled=statuses.count(ShipmentStatus.cancelled),
    )
