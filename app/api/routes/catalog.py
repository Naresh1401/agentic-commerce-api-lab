from fastapi import APIRouter, Depends

from app.core.auth import Principal, require_scopes
from app.domain.models import Product
from app.integrations.catalog_partner import CatalogPartner

router = APIRouter()


@router.get("/products", response_model=list[Product])
def list_products(_: Principal = Depends(require_scopes("orders:read"))) -> list[Product]:
    return CatalogPartner().list_products()

