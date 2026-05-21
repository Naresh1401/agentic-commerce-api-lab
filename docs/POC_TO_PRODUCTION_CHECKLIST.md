# POC To Production Checklist

Use this checklist when explaining how you would help a fast-moving pod.

- API contract reviewed and versioned.
- Authentication and authorization implemented.
- Tenant and object-level access tested.
- Idempotency implemented for write operations.
- Partner adapter contract tests added.
- Timeouts, retries, and fallback behavior documented.
- Structured logs and correlation IDs added.
- Metrics and traces added for endpoint and partner latency.
- Secrets moved out of code and local config.
- Rate limits and abuse controls defined.
- Error model standardized.
- MCP tool descriptions, schemas, and side effects reviewed.
- Human approval added for risky agent actions.
- Load and failure tests run for important flows.
- Runbook written for deployment, rollback, and partner incidents.

