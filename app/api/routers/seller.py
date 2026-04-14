from fastapi import APIRouter

from app.api.tag import APITag
from app.api.schemas.seller import SellerCreate, SellerRead
from ..dependencies import SellerServiceDep

router = APIRouter(prefix="/seller", tags=[APITag.SELLER])


@router.post("/signup", response_model=SellerRead)
async def register_seller(
    seller: SellerCreate,
    service: SellerServiceDep,
):
    return await service.add_seller(seller)
