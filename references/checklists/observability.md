# Observability

- Structured logs with correlation IDs that survive async hops and service boundaries.
- Metrics for rate, errors, duration (RED) on services and utilization, saturation, errors (USE) on resources.
- Distributed tracing across components and queues.
- SLIs and SLOs defined; alerts are symptom-based (user-facing impact) and tied to SLOs; each alert links a runbook.
- Test: could on-call identify what broke within minutes using what exists today? Note what blocks that.
- No sensitive data in logs, traces, or metrics labels; log volume and retention have a cost owner.
