from fastapi import FastAPI

from app.api.routes import catalog, health, mcp_tools, orders, partners
from app.core.errors import register_exception_handlers


def create_app() -> FastAPI:
    app = FastAPI(
        title="Agentic Commerce API Lab",
        version="0.1.0",
        description="Partner-ready commerce APIs with orchestration and MCP tool exposure.",
    )
    register_exception_handlers(app)
    app.include_router(health.router)
    app.include_router(catalog.router, prefix="/v1/catalog", tags=["catalog"])
    app.include_router(orders.router, prefix="/v1/orders", tags=["orders"])
    app.include_router(partners.router, prefix="/v1/partners", tags=["partners"])
    app.include_router(mcp_tools.router, prefix="/mcp", tags=["mcp"])
    return app


app = create_app()

