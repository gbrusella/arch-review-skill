# Performance and scalability

- **Hot paths and complexity:** N+1 queries, unbounded loops or queries, missing pagination, chatty service calls, sync-over-async, work done per request that could be done once.
- **Data access:** missing or wrong indexes, over-fetching, large payloads, transactions or locks held across remote calls.
- **Caching:** what is cached, invalidation strategy, stampede protection, and whether the cache is a correctness dependency or only an optimization.
- **Concurrency:** shared mutable state, thread and connection pool sizing, backpressure, bounded queues.
- **Scaling model:** stateless or sticky; what limits horizontal scaling (single writer, session state, global locks); cost of scaling.
- **Evidence:** load tests, baselines, profiling. Mark every number as **stated** or **recommended**. Static reading finds likely risks; it does not prove a bottleneck, so use `risk` unless measured.
