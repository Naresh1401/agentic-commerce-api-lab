from fastapi import APIRouter, Depends, Header

from app.core.auth import Principal, require_scopes
from app.core.idempotency import IdempotencyStore
from app.domain.models import CheckoutRequest, CheckoutResponse, QuoteRequest, QuoteResponse
from app.orchestration.commerce import CommerceOrchestrator

router = APIRouter()
idempotency_store = IdempotencyStore()


@router.post("/quote", response_model=QuoteResponse)
def quote_order(
    request: QuoteRequest,
    principal: Principal = Depends(require_scopes("orders:read")),
) -> QuoteResponse:
    return CommerceOrchestrator().quote(request, principal)


@router.post("/checkout", response_model=CheckoutResponse)
def checkout(
    request: CheckoutRequest,
    idempotency_key: str = Header(..., alias="Idempotency-Key"),
    principal: Principal = Depends(require_scopes("orders:write")),
) -> CheckoutResponse:
    cached = idempotency_store.get(idempotency_key)
    if cached:
        return CheckoutResponse.model_validate(cached)
    response = CommerceOrchestrator().checkout(request, principal)
    idempotency_store.put(idempotency_key, response.model_dump())
    return response

