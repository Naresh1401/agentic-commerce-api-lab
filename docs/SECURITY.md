# Security Notes

## Auth Pattern

This lab uses demo bearer tokens for local learning. In production, use OAuth 2.0 and validate JWTs or opaque tokens through a trusted identity provider.

Minimum claims or token metadata:

- `sub`: caller identity
- `iss`: trusted issuer
- `aud`: intended API audience
- `exp`: expiration
- `tenant_id`: tenant or partner boundary
- `scope`: allowed actions

## Authorization Layers

- Endpoint scope checks: `orders:read`, `orders:write`, `tools:invoke`.
- Tenant checks: caller can only access assigned tenant.
- Object checks: caller can only access allowed customer/order IDs.
- Side-effect checks: agent tools that write data should require stronger approval than read-only tools.

## MCP And Agent Safety

Treat MCP tools as API endpoints with a natural-language front door:

- Keep tool names boring and explicit.
- Write descriptions that define allowed behavior and side effects.
- Validate every argument with a schema.
- Prefer read-only tools by default.
- Require human approval for payment, cancellation, refund, account update, or partner credential actions.
- Log tool name, caller, tenant, arguments hash, result status, latency, and approval state.

## OWASP API Risks To Know

- Broken object level authorization.
- Broken authentication.
- Broken object property level authorization.
- Unrestricted resource consumption.
- Broken function level authorization.
- Unrestricted access to sensitive business flows.
- Server-side request forgery.
- Security misconfiguration.
- Improper inventory management.
- Unsafe consumption of APIs.

