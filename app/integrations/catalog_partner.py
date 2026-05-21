from decimal import Decimal

from app.domain.models import Product
from app.integrations.contracts import CatalogPort


class CatalogPartner(CatalogPort):
    def list_products(self) -> list[Product]:
        return [
            Product(
                sku="sku-coffee-001",
                name="Cincinnati Blend Coffee",
                price=Decimal("12.99"),
                partner="local-commerce-partner",
            ),
            Product(
                sku="sku-mug-002",
                name="Agentic Commerce Mug",
                price=Decimal("9.50"),
                partner="local-commerce-partner",
            ),
        ]

