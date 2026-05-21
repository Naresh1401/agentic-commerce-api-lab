from decimal import Decimal
from uuid import uuid4

from app.core.auth import Principal
from app.core.errors import CommerceError
from app.domain.models import CheckoutRequest, CheckoutResponse, QuoteLine, QuoteRequest, QuoteResponse
from app.integrations.registry import PartnerRegistry

TAX_RATE = Decimal("0.075")
BASE_SHIPPING = Decimal("4.99")


class CommerceOrchestrator:
    def __init__(self, partners: PartnerRegistry | None = None) -> None:
        self.partners = partners or PartnerRegistry()

    def quote(self, request: QuoteRequest, principal: Principal) -> QuoteResponse:
        self._validate_customer_access(request.customer_id, principal)
        lines: list[QuoteLine] = []
        warnings: list[str] = []

        for item in request.items:
            available_units = self.partners.inventory.available_units(item.sku, request.fulfillment_mode)
            unit_price = self.partners.pricing.unit_price(item.sku)
            available = available_units >= item.quantity and unit_price > 0
            if not available:
                warnings.append(f"{item.sku} cannot be fully reserved")
            lines.append(
                QuoteLine(
                    sku=item.sku,
                    quantity=item.quantity,
                    unit_price=unit_price,
                    extended_price=unit_price * item.quantity,
                    available=available,
                )
            )

        subtotal = sum((line.extended_price for line in lines), Decimal("0.00"))
        tax = (subtotal * TAX_RATE).quantize(Decimal("0.01"))
        shipping = BASE_SHIPPING if request.fulfillment_mode != "pickup" else Decimal("0.00")
        total = subtotal + tax + shipping
        return QuoteResponse(
            quote_id=f"quote_{uuid4().hex[:12]}",
            subtotal=subtotal,
            tax=tax,
            shipping=shipping,
            total=total,
            lines=lines,
            warnings=warnings,
        )

    def checkout(self, request: CheckoutRequest, principal: Principal) -> CheckoutResponse:
        quote = self.quote(request, principal)
        if any(not line.available for line in quote.lines):
            raise CommerceError("INVENTORY_UNAVAILABLE", "One or more items cannot be reserved")
        authorization_id = self.partners.payment.authorize(quote.total, request.payment_method.token)
        fulfillment_ref = self.partners.fulfillment.reserve(
            {line.sku: line.quantity for line in quote.lines},
            request.destination_zip,
        )
        return CheckoutResponse(
            order_id=f"order_{uuid4().hex[:12]}",
            payment_authorization_id=authorization_id,
            fulfillment_reference=fulfillment_ref,
            status="accepted",
            quote=quote,
        )

    def _validate_customer_access(self, customer_id: str, principal: Principal) -> None:
        if principal.tenant_id != "tenant_cincinnati":
            raise CommerceError("TENANT_DENIED", "Principal cannot access this commerce tenant", 403)
        if not customer_id.startswith("cust_"):
            raise CommerceError("CUSTOMER_DENIED", "Customer identifier is outside allowed contract", 403)

