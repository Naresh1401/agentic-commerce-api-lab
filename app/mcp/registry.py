from typing import Any, Literal

from pydantic import BaseModel, Field

from app.core.auth import Principal
from app.domain.models import QuoteRequest
from app.orchestration.commerce import CommerceOrchestrator


class McpToolInvocation(BaseModel):
    name: Literal["commerce.quote"]
    arguments: dict[str, Any] = Field(default_factory=dict)


class McpToolRegistry:
    def tool_manifest(self) -> list[dict[str, object]]:
        return [
            {
                "name": "commerce.quote",
                "description": "Create a non-binding commerce quote from customer, item, and destination inputs.",
                "input_schema": QuoteRequest.model_json_schema(),
                "side_effects": "none",
                "required_scope": "tools:invoke",
            }
        ]

    def invoke(self, invocation: McpToolInvocation, principal: Principal) -> dict[str, object]:
        if invocation.name == "commerce.quote":
            request = QuoteRequest.model_validate(invocation.arguments)
            quote = CommerceOrchestrator().quote(request, principal)
            return {"tool": invocation.name, "result": quote.model_dump(mode="json")}
        raise ValueError(f"Unsupported tool: {invocation.name}")

