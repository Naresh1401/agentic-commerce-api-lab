from app.integrations.contracts import FulfillmentPort, InventoryPort, PaymentPort, PricingPort
from app.integrations.mock_partners import (
    MockFulfillmentPartner,
    MockInventoryPartner,
    MockPaymentPartner,
    MockPricingPartner,
)


class PartnerRegistry:
    def __init__(self) -> None:
        self.inventory: InventoryPort = MockInventoryPartner()
        self.pricing: PricingPort = MockPricingPartner()
        self.payment: PaymentPort = MockPaymentPartner()
        self.fulfillment: FulfillmentPort = MockFulfillmentPartner()

    def names(self) -> list[str]:
        return ["catalog", "inventory", "pricing", "payment", "fulfillment"]

