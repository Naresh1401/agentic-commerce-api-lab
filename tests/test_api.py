from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def auth(token: str = "partner-demo-token") -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_catalog_requires_auth() -> None:
    response = client.get("/v1/catalog/products")
    assert response.status_code == 401


def test_quote_composes_pricing_inventory_tax_and_shipping() -> None:
    response = client.post(
        "/v1/orders/quote",
        headers=auth(),
        json={
            "customer_id": "cust_100",
            "items": [{"sku": "sku-coffee-001", "quantity": 2}],
            "destination_zip": "45202",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["subtotal"] == "25.98"
    assert body["tax"] == "1.95"
    assert body["shipping"] == "4.99"
    assert body["total"] == "32.92"


def test_checkout_requires_write_scope() -> None:
    response = client.post(
        "/v1/orders/checkout",
        headers={**auth("analyst-demo-token"), "Idempotency-Key": "demo-1"},
        json={
            "customer_id": "cust_100",
            "items": [{"sku": "sku-coffee-001", "quantity": 1}],
            "destination_zip": "45202",
            "payment_method": {"token": "tok_12345678"},
        },
    )
    assert response.status_code == 403


def test_checkout_is_idempotent_for_same_key() -> None:
    payload = {
        "customer_id": "cust_100",
        "items": [{"sku": "sku-coffee-001", "quantity": 1}],
        "destination_zip": "45202",
        "payment_method": {"token": "tok_12345678"},
    }
    headers = {**auth(), "Idempotency-Key": "same-key-1"}
    first = client.post("/v1/orders/checkout", headers=headers, json=payload)
    second = client.post("/v1/orders/checkout", headers=headers, json=payload)
    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["order_id"] == second.json()["order_id"]

