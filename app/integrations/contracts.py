from abc import ABC, abstractmethod
from decimal import Decimal

from app.domain.models import FulfillmentMode, Product


class CatalogPort(ABC):
    @abstractmethod
    def list_products(self) -> list[Product]:
        raise NotImplementedError


class InventoryPort(ABC):
    @abstractmethod
    def available_units(self, sku: str, fulfillment_mode: FulfillmentMode) -> int:
        raise NotImplementedError


class PricingPort(ABC):
    @abstractmethod
    def unit_price(self, sku: str) -> Decimal:
        raise NotImplementedError


class PaymentPort(ABC):
    @abstractmethod
    def authorize(self, amount: Decimal, payment_token: str) -> str:
        raise NotImplementedError


class FulfillmentPort(ABC):
    @abstractmethod
    def reserve(self, sku_quantities: dict[str, int], destination_zip: str) -> str:
        raise NotImplementedError

