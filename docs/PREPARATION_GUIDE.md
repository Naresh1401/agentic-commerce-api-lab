# Preparation Guide

This is a focused joining plan for the Agentic AI API Developer role.

## Week 1: API-First Commerce Foundations

Build and explain:

- Versioned REST endpoints using FastAPI.
- OpenAPI schema review at `/docs` and `/openapi.json`.
- Request/response models with Pydantic validation.
- Standard error responses and status codes.
- Idempotency for checkout operations.

Practice questions:

- How would you design a partner-ready checkout API?
- What belongs in an API contract before implementation starts?
- How do you handle backward-compatible API changes?
- What makes a POC production-ready?

## Week 2: Auth, Authorization, And API Security

Build and explain:

- Bearer token validation.
- OAuth 2.0 client credentials flow conceptually.
- JWT claims: subject, audience, issuer, expiry, tenant, scopes.
- RBAC vs ABAC vs object-level authorization.
- OWASP API risks, especially broken object level authorization, broken authentication, unrestricted resource consumption, and unsafe consumption of APIs.

Practice questions:

- How would you secure a third-party partner API?
- What is the difference between authentication and authorization?
- How would you prevent a partner from seeing another tenant's customer orders?
- What should be logged, and what should never be logged?

## Week 3: Orchestration And Integrations

Build and explain:

- Adapter pattern around catalog, inventory, pricing, payment, and fulfillment.
- Retry and timeout strategy for partner calls.
- Circuit breaker and fallback thinking.
- Contract tests between internal API and partner adapters.
- Webhook ingestion and replay protection.

Practice questions:

- Why avoid brittle point-to-point integrations?
- How would you onboard a new commerce partner quickly?
- How do you handle partial failure in a checkout workflow?
- How do you make partner POCs repeatable?

## Week 4: MCP And Agentic Workflows

Build and explain:

- MCP server responsibilities.
- Tool manifest: name, description, input schema, side effects, required scope.
- Tool invocation and validation.
- Safe tool design for read-only vs write actions.
- Human approval gates for payment, refund, cancellation, or account changes.

Practice questions:

- How does an agent consume an API through an MCP server?
- What makes a good tool description?
- How do you prevent prompt injection from triggering unsafe tools?
- How would you test an agentic commerce workflow?

## 30-60-90 Day Plan

First 30 days:

- Learn the commerce domain, partner APIs, existing auth patterns, deployment standards, and observability stack.
- Ship small improvements: docs, test gaps, endpoint fixes, sandbox partner setup.

Days 31-60:

- Own a vertical integration slice such as quote or order status.
- Add contract tests, idempotency, telemetry, and MCP tool exposure.
- Help turn one partner POC into a reusable template.

Days 61-90:

- Lead a production hardening pass for a partner integration.
- Define MCP tool safety guidelines and test strategy.
- Document a repeatable partner onboarding playbook.

## Interview Answers To Rehearse

Tell me about yourself:

> I am a backend and AI integration developer with experience building REST APIs, secure integrations, orchestration services, and agentic/AI-assisted workflows. My recent work connects enterprise systems through APIs, uses OAuth/JWT-style access patterns, and exposes business capabilities to AI tools. This role is a strong fit because it combines API-first engineering, commerce integrations, and MCP-style agent enablement.

Describe an orchestration layer:

> An orchestration layer owns a business flow that crosses multiple services. For checkout, it may call catalog, inventory, pricing, payment, and fulfillment services, then return one stable response to the consumer. The value is that partner clients and agents do not need to understand every downstream system.

How do you test agentic systems:

> I separate deterministic contracts from probabilistic behavior. API schemas, auth checks, permissions, idempotency, and side effects must be deterministic. For agent behavior, I use golden scenarios, adversarial prompts, tool-call assertions, and human approval checks for risky actions.

