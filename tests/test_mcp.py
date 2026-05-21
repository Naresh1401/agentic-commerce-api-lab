from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_mcp_tool_manifest_is_agent_consumable() -> None:
    response = client.get("/mcp/tools", headers={"Authorization": "Bearer partner-demo-token"})
    assert response.status_code == 200
    tool = response.json()["tools"][0]
    assert tool["name"] == "commerce.quote"
    assert tool["side_effects"] == "none"
    assert "input_schema" in tool


def test_mcp_quote_tool_validates_agent_arguments() -> None:
    response = client.post(
        "/mcp/invoke",
        headers={"Authorization": "Bearer partner-demo-token"},
        json={
            "name": "commerce.quote",
            "arguments": {
                "customer_id": "cust_200",
                "items": [{"sku": "sku-coffee-001", "quantity": 1}],
                "destination_zip": "45202",
            },
        },
    )
    assert response.status_code == 200
    assert response.json()["result"]["total"] == "18.95"
