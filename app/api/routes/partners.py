from fastapi import APIRouter, Depends

from app.core.auth import Principal, require_scopes
from app.integrations.registry import PartnerRegistry

router = APIRouter()


@router.get("")
def list_partners(_: Principal = Depends(require_scopes("orders:read"))) -> dict[str, list[str]]:
    return {"partners": PartnerRegistry().names()}

