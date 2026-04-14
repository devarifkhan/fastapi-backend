from fastapi import APIRouter

router = APIRouter(prefix="/seller")

@app.post("/seller/signup")
def register_seller(
    seller: SellerCreate,
    service: SellerServiceDep
):
    service.add_seller(seller)