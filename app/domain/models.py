from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, Field, field_validator


class FulfillmentMode(StrEnum):
    pickup = "pickup"
    ship = "ship"
    same_day = "same_day"


class Product(BaseModel):
    sku: str
    name: str
    price: Decimal
    currency: str = "USD"
    partner: str


class OrderItem(BaseModel):
    sku: str
    quantity: int = Field(gt=0, le=50)


class QuoteRequest(BaseModel):
    customer_id: str
    items: list[OrderItem] = Field(min_length=1, max_length=20)
    destination_zip: str = Field(min_length=5, max_length=10)
    fulfillment_mode: FulfillmentMode = FulfillmentMode.ship

    @field_validator("destination_zip")
    @classmethod
    def zip_must_be_numeric_prefix(cls, value: str) -> str:
        prefix = value[:5]
        if not prefix.isdigit():
            raise ValueError("destination_zip must start with five digits")
        return value


class QuoteLine(BaseModel):
    sku: str
    quantity: int
    unit_price: Decimal
    extended_price: Decimal
    available: bool


class QuoteResponse(BaseModel):
    quote_id: str
    subtotal: Decimal
    tax: Decimal
    shipping: Decimal
    total: Decimal
    currency: str = "USD"
    lines: list[QuoteLine]
    warnings: list[str] = []


class PaymentMethod(BaseModel):
    token: str = Field(min_length=8)
    type: str = "card"


class CheckoutRequest(QuoteRequest):
    payment_method: PaymentMethod


class CheckoutResponse(BaseModel):
    order_id: str
    payment_authorization_id: str
    fulfillment_reference: str
    status: str
    quote: QuoteResponse

