# Architecture

## Logical View

```text
Agent / Partner Client
        |
        v
REST API or MCP Tool Shim
        |
        v
Commerce Orchestrator
        |
        +--> Catalog Adapter
        +--> Inventory Adapter
        +--> Pricing Adapter
        +--> Payment Adapter
        +--> Fulfillment Adapter
```

## Design Choices

- FastAPI: practical API-first framework with OpenAPI generation and strong type validation.
- Pydantic: request/response contracts double as validation boundaries for agent-generated inputs.
- Adapter pattern: downstream partners are replaceable behind stable ports.
- Orchestrator: business flows are centralized instead of spread across route handlers.
- MCP shim: agent-facing tools reuse the same domain contracts as REST endpoints.
- Idempotency: checkout accepts `Idempotency-Key` so retries do not duplicate orders.

## Production Extensions

Add these before real deployment:

- Real OAuth 2.0/JWT validation against an identity provider.
- Persistent idempotency storage such as Redis or Postgres.
- Structured logging with correlation IDs.
- OpenTelemetry traces around each partner call.
- Timeout, retry, circuit breaker, and bulkhead policies.
- Secret management through AWS Secrets Manager, Azure Key Vault, or Vault.
- Contract tests against partner sandboxes.
- Rate limiting and API gateway policy enforcement.

