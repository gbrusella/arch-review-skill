# Specialized subagents (optional)

Referenced from step 6 of `SKILL.md`. When subagents are available and the repository is large or the review is Full depth, split the work into specialists that run in parallel. Skip this for small repositories or Quick depth; one reviewer is cheaper and more consistent. If subagents are forbidden or unavailable, one reviewer covers every specialist's checklists serially.

## Split

**security** (secrets handling, OWASP, supply chain, regulated data, LLM/AI), **infrastructure** (deployment strategy, cloud framework alignment, IaC, containers, CI/CD, operations and resilience, observability, cost), **runtime** (performance and scalability, data architecture, resilience in code), **architecture** (boundaries, coupling, maintainability and evolvability, integrations and migration, local data, ADR and MADR checks), **testing** (testing and coverage), **requirements** (usage and volume, NFRs, auditability and traceability). Merge or drop specialists to match the topics that apply.

## Briefing

Brief each one with: the target and depth, the inventory from step 2, the guidelines from step 3, its checklist sections, the Vocabulary section verbatim, the read-only rule, and the instruction never to print secret values.

## Return format

Each returns findings only (location, evidence status, type, category, severity, likelihood, confidence, method, one-line statement, detail), plus its own Limitations and `unverifiable` items. Specialists do not write the report, verdict, or remediation plan.

## Merge

Do the merge yourself: deduplicate findings reported by more than one specialist (keep the highest severity and cite all locations), resolve conflicts by re-checking the cited evidence, renumber IDs, then write every Output section, the verdict, and the remediation plan from the merged set.

Treat subagent output as unverified until you spot-check each `high` finding against the cited code or document.
