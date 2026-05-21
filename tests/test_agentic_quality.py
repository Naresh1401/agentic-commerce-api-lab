from pydantic import ValidationError
import pytest

from app.domain.models import QuoteRequest


@pytest.mark.parametrize(
    "agent_arguments",
    [
        {"customer_id": "cust_1", "items": [], "destination_zip": "45202"},
        {"customer_id": "cust_1", "items": [{"sku": "sku-coffee-001", "quantity": 0}], "destination_zip": "45202"},
        {"customer_id": "cust_1", "items": [{"sku": "sku-coffee-001", "quantity": 1}], "destination_zip": "CINCI"},
    ],
)
def test_agent_generated_arguments_are_rejected_at_contract_boundary(agent_arguments: dict) -> None:
    with pytest.raises(ValidationError):
        QuoteRequest.model_validate(agent_arguments)

