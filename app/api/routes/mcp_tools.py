from fastapi import APIRouter, Depends

from app.core.auth import Principal, require_scopes
from app.mcp.registry import McpToolInvocation, McpToolRegistry

router = APIRouter()


@router.get("/tools")
def tools(_: Principal = Depends(require_scopes("tools:invoke"))) -> dict[str, object]:
    return {"tools": McpToolRegistry().tool_manifest()}


@router.post("/invoke")
def invoke_tool(
    invocation: McpToolInvocation,
    principal: Principal = Depends(require_scopes("tools:invoke")),
) -> dict[str, object]:
    return McpToolRegistry().invoke(invocation, principal)

