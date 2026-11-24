# Checklist index

Read every checklist unless a stated skip reason applies (for example no LLM calls, no local data, no cloud provider, a single-ADR target). Record each skip reason in Scope. "Little to review" is not a skip reason: a short checklist on a small project is quick, and a missing control is a finding. Each file is self-contained.

| Topic | File | Applies |
|---|---|---|
| NFRs | `nfrs.md` | unless a skip reason applies |
| Usage and volume | `usage-and-volume.md` | unless a skip reason applies |
| Security and privacy | `security-and-privacy.md` | unless a skip reason applies |
| Secrets handling | `secrets-handling.md` | unless a skip reason applies |
| Secure data handling (OWASP Top 10 hygiene) | `secure-data-handling.md` | unless a skip reason applies |
| Infrastructure and CI config | `infrastructure-and-ci.md` | only if IaC, container, or pipeline files exist |
| LLM and AI features | `llm-and-ai.md` | only if the project calls an LLM or ships AI-driven behavior |
| Regulated data | `regulated-data.md` | only if PHI, PII, or other regulated data is indicated |
| Auditability and traceability | `auditability-and-traceability.md` | unless a skip reason applies |
| Performance and scalability | `performance-and-scalability.md` | unless a skip reason applies |
| Operations and resilience | `operations-and-resilience.md` | unless a skip reason applies |
| Deployment strategy and cloud alignment | `deployment-and-cloud.md` | Part A: any deployed software; Parts B-C: only if a cloud provider is detected |
| Observability | `observability.md` | unless a skip reason applies |
| Data architecture | `data-architecture.md` | unless a skip reason applies |
| Integrations and migration | `integrations-and-migration.md` | unless a skip reason applies |
| Local data | `local-data.md` | only if a feature reads or otherwise accesses local data |
| Testing and coverage | `testing-and-coverage.md` | unless a skip reason applies |
| Architecture and design | `architecture-and-design.md` | always, except a single-ADR target |
| Maintainability and evolvability | `maintainability-and-evolvability.md` | unless a skip reason applies |
| Supply chain | `supply-chain.md` | unless a skip reason applies |
| Cost | `cost.md` | unless a skip reason applies |
