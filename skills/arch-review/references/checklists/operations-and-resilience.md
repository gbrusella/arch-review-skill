# Operations and resilience

Deployment topology and environments, support ownership, backup/restore,
disaster recovery, failure modes, rollback, recovery objectives. Name the documents needed to verify each
and state what cannot be confirmed without them.

- **Outbound calls:** every one has a timeout, a bounded retry with backoff and jitter, and a circuit breaker or bulkhead where failure could cascade.
- **Safe retries:** idempotency keys, duplicate handling, outbox/inbox for messaging, at-least-once semantics handled.
- **Failure modes:** single points of failure, cascading-failure paths, behavior when each dependency is down, graceful degradation or a defined degraded mode.
- **Partial failure:** multi-step workflows (sagas, compensation), poison messages and dead-letter handling, stuck-state recovery.
- **Recovery:** backups exist, restore was tested (no tested restore means RTO/RPO is `unverifiable`), DR plan and ownership.
- **Deploy safety:** rollback path, expand/contract schema migrations, feature flags, canary or staged rollout, blast radius per deploy.
- **Capacity protection:** rate limiting, load shedding, quotas per tenant or client, noisy-neighbor isolation.
- **Failure testing:** chaos or game-day evidence; health checks that reflect real readiness, not just process liveness.
