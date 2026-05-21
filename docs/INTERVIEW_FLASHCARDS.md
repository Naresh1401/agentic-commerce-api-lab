# Interview Flashcards

Q: What is API orchestration?
A: A service layer that composes multiple downstream APIs into one business-level flow, such as checkout.

Q: Why use adapters for partners?
A: They isolate partner-specific protocols, errors, and data formats behind stable internal contracts.

Q: What is MCP?
A: An open standard for connecting AI applications to external systems through tools, data, and workflows.

Q: What makes a tool safe for agents?
A: Clear schema, narrow purpose, explicit side effects, authorization checks, validation, logging, and approval gates for risky actions.

Q: How do you handle partner retries?
A: Use timeouts, retry only safe operations, use idempotency keys for writes, and track correlation IDs.

Q: How do you move POC to production?
A: Add auth, tests, observability, deployment automation, secrets management, error handling, rate limits, and operational runbooks.

Q: What is BOLA?
A: Broken object level authorization, where a caller can access another user's object by changing an identifier.

Q: How do you test agentic variability?
A: Validate deterministic API boundaries, assert allowed tool calls, run golden scenarios, test adversarial prompts, and require approvals for high-risk actions.

