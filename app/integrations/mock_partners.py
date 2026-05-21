from decimal import Decimal

from app.domain.models import FulfillmentMode
from app.integrations.contracts import FulfillmentPort, InventoryPort, PaymentPort, PricingPort


class MockInventoryPartner(InventoryPort):
    inventory = {"sku-coffee-001": 20, "sku-mug-002": 0}

    def available_units(self, sku: str, fulfillment_mode: FulfillmentMode) -> int:
        if fulfillment_mode == FulfillmentMode.same_day and sku == "sku-coffee-001":
            return 5
        return self.inventory.get(sku, 0)


class MockPricingPartner(PricingPort):
    prices = {"sku-coffee-001": Decimal("12.99"), "sku-mug-002": Decimal("9.50")}

    def unit_price(self, sku: str) -> Decimal:
        return self.prices.get(sku, Decimal("0.00"))


class MockPaymentPartner(PaymentPort):
    def authorize(self, amount: Decimal, payment_token: str) -> str:
        if amount <= 0:
            raise ValueError("amount must be positive")
        return f"auth_{payment_token[-4:]}_{str(amount).replace('.', '')}"


class MockFulfillmentPartner(FulfillmentPort):
    def reserve(self, sku_quantities: dict[str, int], destination_zip: str) -> str:
        sku_count = len(sku_quantities)
        return f"fulfill_{destination_zip[:5]}_{sku_count}"

