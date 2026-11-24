---
name: arch-review
description: Use when asked for an architecture review, compliance assessment, or ADR/design-doc review of a project, feature, pull request, or decision, including NFR, security, performance, resilience, maintainability, traceability, testing, or operational-readiness gaps.
---

# Architecture Review

Review a project from its source code and documentation. Version history is in `CHANGELOG.md`.

**Read-only.** Do not modify project files. Read-only commands (`git log`, `git grep`, `grep`, file listing) and secret or dependency scanners that are already installed are allowed, provided they need no network and write nothing to the repository. Do not install tools. The one exception is saving the report (see Saving), and only after the user agrees to the path.

## Stop conditions

- If the target has no source code and no documentation, output only **Summary** saying so, and stop.
- If code conflicts with a documented decision, report a finding citing both the code location and the document section.

## Rules of conduct

- One issue per finding. If parts of a candidate finding differ in evidence status, severity, or fix, split it (for example N+1 queries, unpinned base image, and unpinned dependencies are three findings, not one).
- Before marking a finding `confirmed`, re-open the cited line or section and state the minimal trigger (for example the request or input that exploits it). If you cannot, use `risk`. A claim that depends on a version, configuration, or runtime you did not read or resolve (for example behavior of an unpinned dependency) is `risk`.
- Rate a finding on the fact you verified (for example "no idempotency key is sent" is `confirmed`). Describe consequences that depend on third-party or runtime behavior you could not see (for example "PayCo may charge twice") in the detail, marked as such; they do not downgrade the fact, and they do not upgrade a guess.
- Merge candidates into one finding when they share a root cause and a component, even if the fix has several steps (list the steps in the plan; for example one leaked password literal that appears in two places, or several injectable queries of one kind). Keep them separate when the evidence status differs (one `confirmed`, one `risk`) or when the fixes are independent work by different owners.
- Refer to people by role, never by name, in the report and in the findings file. If a source names an individual as owner, write the role (or "a named individual" if no role is stated).
- Never print secret values. Use the redacted recipes in `references/checklists/secrets-handling.md`.
- No style nits, no rewrite recommendations without evidence, no compliance or certification claims.
- Do not treat missing information as evidence that a requirement is met.
- Never skip an applicable checklist to save time. If one is skipped, record it under Limitations with the reason. List the checklists you read and skipped in Scope.
- Subagents are optional. If they are unavailable or the caller forbids them, work serially; do not drop coverage.
- Facts about a provider or platform (framework pillars, plan or service limits, default behavior) come from official documentation when a read-only lookup is possible. Otherwise state them as `assumption`. Never present such a fact from memory as verified.
- If the repository holds its own review or finding list, read it, cite its items as `repo <id>` (keep your own IDs), and treat any item not marked done there as open.
- Non-interactive runs (no user to ask): wherever this skill says to ask the user, do not ask; record what you assumed (or that nothing was available) in Scope and continue.

## Vocabulary (use everywhere)

**Evidence status** — exactly one per finding:
- `confirmed`: verified in code or documents.
- `risk`: plausible problem, not proven.
- `unverifiable`: a documented or expected requirement cannot be checked from available material.
- `assumption`: something you had to assume. State it. Use in Scope and Limitations, not as a finding status.

**Finding type:** `design-defect` | `doc-gap` | `unverifiable`. Valid combinations: `design-defect` with `confirmed` or `risk`; `doc-gap` with `confirmed`; `unverifiable` with `unverifiable`. For `unverifiable`, say in the statement which kind it is: `claimed but not evidenced` (a document asserts it) or `expected but absent` (nothing asserts it). A `doc-gap` is `confirmed` when you read the documents and the item is absent.

**Severity:** impact on the target context if the issue occurs, judged against the system's priority quality attributes (Process step 1).
- `high`: endangers or blocks the decision; security, regulated data, data loss, money movement, or a core decision driver.
- `medium`: should fix before relying on the design.
- `low`: improvement.
- A `confirmed` finding that exposes credentials or tokens (including in logs, images, or committed files), bypasses authorization, allows injection, or risks data loss or money loss is `high` regardless of likelihood.
- The same kind of finding as an unconfirmed `risk` is `high` only if likelihood is `medium` or higher; otherwise `medium`. Credentials held as plain application settings or CI secrets (not committed, not broadly readable) are `medium`; committed or broadly readable ones are `high`.
- Otherwise lower severity by one level when likelihood is `low`.

**Likelihood:** `high` | `medium` | `low`, how likely the issue is to occur or be exploited in the target context. A `confirmed` defect on a hot path or exposed surface is `high`; one needing rare conditions is `low`. For batch or rarely run systems judge by how often the trigger condition occurs (a failed weekly run, a bad deploy), not by request volume. Required for `design-defect`, including `risk` ones (for a `risk`, rate how likely the stated trigger is under the documented load). `n/a` for `doc-gap` and `unverifiable`.
**Confidence:** `high` | `medium` | `low`, how sure you are the finding is correct. Required for every finding. Confidence is about correctness; likelihood is about whether it will bite.
**Category:** `security` | `supply-chain` | `performance` | `resilience` | `maintainability` | `observability` | `data` | `cost` | `testing` | `requirements` | `operations`. Exactly one per finding.
**Method:** `read` (from code or documents) or `measured` (a tool or test was run; name it). Never present a static estimate as measured.
**Status:** `open` unless a re-review marks it `fixed`. On a first review every finding is `open`.

**Missing information rule:** if a documented or expected requirement cannot be checked, it is a finding of type `unverifiable`. If a whole topic is out of scope or inaccessible (for example no Jira access), it is a Limitation.

**Severity examples for design findings** (calibrate, do not copy blindly):
- `high`: no timeout or circuit breaker on a payment or identity provider call; unbounded query on a request path of a high-volume table; backups exist but restore never tested for a system with a stated RPO; non-idempotent retry on a money-moving operation.
- `medium`: no pagination on an internal list endpoint; alerts on causes (CPU) with none on user-facing symptoms; dependency cycle between core modules; no correlation IDs across async hops.
- `low`: inconsistent naming, minor duplication, missing runbook links for low-impact alerts.

**Severity of `unverifiable` findings:** rate by the impact if the requirement turned out to be unmet, not by the lack of evidence.
- `high`: the requirement guards security, regulated data, data loss, money movement, or a core decision driver (for example an unchecked authorization boundary, or no evidence of backup restore for a payment system).
- `medium`: it affects a stated NFR or operational readiness.
- `low`: it is minor or cosmetic.
When the whole code base is unavailable, record OWASP items as `unverifiable` at the severity their category would carry, and say so in Limitations.

## Process

1. **Scope.** Confirm the target and depth. Target is the whole project, one ADR, one feature, or a diff/PR; for a diff or PR follow `references/delta-review.md` instead of the steps below. If unstated, review the whole project and say so.
   - **Target context:** what the verdict is for: prototype, production at current load, or scale-up. If unstated, assume production at the documented load and say so.
   - **Priority quality attributes:** the 2-3 attributes that drive this system (for example latency over cost, availability over consistency), from the documents or by asking the user. If neither works, infer from the code and mark them `assumption`. Judge findings against these.
   - **Depth:**
     - **Quick:** triage across all quality attributes. Produce Summary, Scope, ADR and guideline checks, a top-risks pass (highest-impact items only from security, performance, resilience, and maintainability), Findings, Recommendations and remediation, and Limitations. List every other section under Limitations as not reviewed.
     - **Full:** every applicable section. Minimum evidence: read the entry points, the deployment and infrastructure files, the files named by ADRs and specs, and the most-changed source files; list in Limitations what you sampled instead of reading fully. Sections 4, 7, and 9 collapse to one line in Scope when they would only repeat other sections.
     - **Compact:** the default for small targets (a single ADR, a feature, or a repository of roughly 30 source files or fewer, even if Full was requested, unless the user insists on the full format). Use the Compact format in Output.
   - Detect which optional topics apply (see `references/checklists/README.md`) and record each skipped topic with a reason.
   - **Re-review:** if a previous report or findings file exists, reuse its finding IDs, match findings by `key` (see `references/findings-schema.md`), and mark each `fixed`, `open`, or `new`.
2. **Inventory.** Identify languages, frameworks, entry points, major components, external dependencies, and relevant documents: ADRs, feature specs, runbooks, `AGENTS.md`, repository conventions.
   - **Deployment and cloud:** note how the project is deployed (pipeline files, IaC, Dockerfiles, manifests, deployment docs) and detect the cloud provider from repository evidence (`references/checklists/deployment-and-cloud.md`, Part B). Record both in Scope.
   - **System context:** note what calls this target (upstream) and what it calls (downstream), including data stores and third parties. Ask the user if unclear; otherwise infer from code and config and mark `assumption`.
   - **History as evidence:** churn hotspots, excluding docs, lockfiles, and generated output (for example `git log --format= --name-only -- . ':!*.md' ':!docs' ':!*lock*' ':!*-out' | sort | uniq -c | sort -rn | head`; drop paths that no longer exist in `git ls-files` so renames do not distort the result), reverts, hotfix commits, long-lived TODOs. With fewer than about 20 commits write "not applicable".
3. **Guidelines.** Look for organization or architecture guidelines in the repository. If none are found, ask the user for them (non-interactive: do not ask). If still none, say so and review against MADR and general practice only. `references/frameworks.md` maps categories to common frameworks if the organization uses one.
4. **ADRs.** Check each ADR against MADR: title, status, context and problem statement, decision drivers, considered options, decision outcome, consequences. Do not require optional sections the repository's own template omits. Also check decision quality: the options are real (not straw men), the consequences name negative outcomes and reversibility, and the decision is consistent with the code.
5. **Features and requirements.** For each feature behind an ADR or design, find its requirement or description. Follow Jira keys or links when reachable, using them only for feature context. If Jira is unreachable, ask the user to paste the issue (non-interactive: report the gap). Do not infer undocumented requirements.
6. **Topic checks.** Check the deployment strategy (documented versus implemented) and, if a cloud provider was detected, alignment with its well-architected framework (`deployment-and-cloud.md`). Load the applicable files from `references/checklists/` (the index in `README.md` lists topic, file, and when each applies) and work through them; read them in Compact too, and do not substitute memory for them. Skip a topic only for a stated skip reason (see the checklist index) and record it in Scope. Always read `architecture-and-design.md` unless the target is a single ADR.
   - **Specialized subagents (optional).** For a large repository or Full depth, when subagents are available, split the work into parallel specialists. Follow `references/subagents.md`. Skip for small repositories, Compact, or Quick depth.
7. **Scenario pass.** Walk 3-5 concrete scenarios through the architecture and record what happens at each step: a key dependency is down for 10 minutes; traffic rises 10x; a bad deploy ships and must be rolled back; a data store loses its latest backup window; one tenant or client misbehaves. Pick the scenarios that stress the priority quality attributes. Where the code or documents cannot answer, record an `unverifiable` finding. Tag each scenario result `confirmed` only if the code shows it; otherwise `risk`. In Compact, 2-3 scenarios.
8. **Ground and classify.** Before writing the Findings table, run a validity check: every `design-defect` has a likelihood and `doc-gap` and `unverifiable` findings have `n/a`; every finding has a confidence, one category, and a valid type/evidence combination; no `confirmed` finding depends on an unread version, setting, or runtime. Cite files, symbols, ADR sections, and Jira keys for every item. Assign finding IDs (`F1`, `F2`, ...) in discovery order as you go; IDs never change afterwards. Give each finding the fields in Vocabulary. Also note what is done well.
9. **Prioritize.** Order recommendations by impact, then effort. State benefit, trade-offs, and likely scope. Avoid broad rewrites without evidence. Pick the three actions that most reduce risk.

## Output

Report each issue once, in the section matching its topic, with its finding ID. Exception: an ADR-versus-code conflict gets a one-line row in section 3 and the detail in the topic section. Write the Findings index and heatmap after all IDs exist.

### Full format

1. **Summary:** fits on one screen; everything else is appendix. Start with one verdict line chosen from the highest open severity: `Not ready` (any open `high`), `Ready with conditions` (open `medium`, no `high`), or `Ready` (only `low` or none). A `high` finding that is already tracked in the repository or its documents, with an owner and a step scheduled before the target context takes effect (for example a go-live checklist item), counts as `Ready with conditions`, not `Not ready`: list it as a condition and say so in the verdict line. An **owner** is a role (for example "Platform lead" or "Data owner"), never a named individual; a role stated in the tracking document counts, but a placeholder such as "TBD" or "someone" does not. **Scheduled** means a date, a release, or a gate that is enforced (for example a setting that keeps a feature off until the item closes). A tracked item blocked on a third party counts only if the blocking dependency itself has an owner role. Untracked, unowned, or unscheduled `high` findings always count. The "Owner (suggested)" column in the plan is your suggestion and never makes a finding tracked. Severity itself is never lowered for this. Name the target context. Then:
   - **Top 3 actions:** the three highest-impact next steps, each with finding IDs.
   - **Quality-attribute heatmap:** a table of category | priority for this system | rating (`strong`, `adequate`, `weak`, `unverifiable`, `not assessed`) | key finding IDs, one row per category in Vocabulary (in Compact, only categories that have findings). Priority is `high`, `medium`, or `low` as set in Scope. Rating: `weak` if any open `high` or two or more open `medium`; `adequate` if the worst open finding is a single `medium` or `low`; `strong` only with positive evidence and no open findings; `unverifiable` if the category rests only on `unverifiable` findings; `not assessed` if no checklist covered it or it does not apply.
   - **Strengths:** 2-5 decisions or practices worth protecting, each with evidence. Omit the section when nothing is strong; do not pad.
2. **Scope:** target, depth, context, checklists read and skipped, deployment approach, cloud provider detected (or none) and how you know, priority attributes, guidelines used, assumptions, system context (upstream and downstream), and skipped topics as a table (topic | applies | reason).
3. **ADR and guideline checks:** a table of item | status (`compliant`, `concern`, `unverifiable`) | evidence. One line for `compliant`; detail for `concern` and `unverifiable`, pointing to the section holding the detail.
4. **Features, usage, and volume:** feature and Jira context, usage patterns, volume assumptions; missing information called out.
5. **NFRs:** measurable targets and verification methods; vague or missing ones called out. Mark targets **stated** or **recommended**. If the repository has its own NFR document, reference it and list only gaps, undecided items, and unverified targets.
6. **Security, privacy, and regulatory:** considerations, unanswered questions, evidence gaps. Include **secrets handling** and **secure data handling (OWASP Top 10)** subsections, mapping code-level issues to the OWASP category. Never print secret values. Never assert compliance.
7. **Auditability and traceability:** audit-trail expectations and gaps; trace links across requirements, decisions, implementation, tests, deployment, operations.
8. **Operations, resilience, and integration:** deployment strategy (documented, implemented, gaps), readiness, resilience (timeouts, retries, failure modes, recovery), observability, integrations, migration, infrastructure and CI config, LLM/AI features when present; the scenario-pass results; what cannot be verified.
9. **Local data:** data model, filtering criteria and defaults, text-search semantics. "Not applicable" if no feature reads local data; add no findings.
10. **Architecture, performance, and maintainability:** subsections for **Architecture and design**, **Performance and scalability**, **Data architecture**, **Maintainability and evolvability** (including churn hotspots and dependency health), **Supply chain**, **Cost**, and, when a cloud provider is detected, **Cloud framework alignment** (a table of pillar | rating `aligned`, `partial`, `gap`, `unverifiable` | evidence | finding IDs, with the line that this is an evidence-based check and not a formal Well-Architected Review). Omit a subsection only with a reason in Scope.
11. **Testing and coverage:** test inventory and CI gating; coverage data source (report or static estimate); a risk-to-test map for critical paths and requirements; **Coverage gaps**; and **Superfluous and redundant tests** (each candidate, the test that still covers the behavior, and the action: consolidate, rewrite, or delete). "Not applicable" if the project has no executable code.
12. **Findings:** index of every finding, most severe first. Per finding: ID, severity, likelihood, type, category, evidence status, confidence, one-line statement, location, and a pointer to the section holding the detail. Under the table add a short detail paragraph (evidence, trigger, impact) for `high` findings only; the detail of other findings lives in their topic section.
13. **Recommendations and remediation plan:** one sequenced table, not two lists. Each row carries the rationale (benefit and trade-offs) in its action column and references finding IDs; do not restate finding detail.
    - Phases: **Now** (every open `high`, plus anything that blocks other work, such as secret rotation), **Next** (open `medium`), **Later** (`low` and improvements).
    - Per item as a table row: plan ID (`R1`, ...), finding IDs, concrete action with benefit and trade-offs, suggested owner role, effort (`S` under a day, `M` a few days, `L` more), dependencies, and a verification step.
    - Order by dependency, then severity, then effort. Group items that touch the same component.
    - Include a doc-only or investigation item for each `unverifiable` finding.
    - Use effort sizes, not dates, unless the user gives a schedule. The plan is a proposal; apply no change.
14. **Limitations:** missing documents or context that lower confidence; tools not run (for example no network audit); skipped topics with reasons.

### Compact format

For small targets, produce:
1. **Summary** (verdict, target context, Top 3 actions, Strengths; heatmap only for categories with findings).
2. **Scope** (one short block: target, context, priority attributes, assumptions, checklists read and skipped, skipped topics in one line each, and one line per ADR: status `compliant`, `concern`, or `unverifiable` with finding IDs).
3. **Findings:** the index table. Add a detail paragraph (evidence, trigger, impact) only for `high` findings; for the rest the statement and location are enough. Include, for usage, volume, or NFR gaps, one `requirements` finding (not a separate section). If there are no ADRs, treat design and deployment documents as the documents to check against, and say so. ADR-versus-code conflicts appear here with both citations.
4. **Scenarios:** 2-3 scenario results, one short paragraph each.
5. **Deployment and cloud:** only if applicable, a short paragraph on deployment strategy (documented versus implemented) and, for a detected cloud provider, a pillar | rating table. In Full, this content belongs in sections 8 and 10.
6. **Recommendations and remediation plan** merged into one table of at most about 10 rows, grouping findings by component or fix: phase, plan ID, finding IDs, action and benefit, owner, effort, depends on, verification.
7. **Limitations.**

Omit any section with nothing to report; do not write "Not applicable" blocks.

### Example

Summary opening:

> **Verdict: Not ready** for production at the documented load. One open `high` finding (F1) leaves an authorization boundary unverified. The other findings are a documentation gap (F2) and a dependency-direction issue (F3).

Findings rows:

| ID | Severity | Likelihood | Type | Category | Evidence | Confidence | Statement | Location | Detail |
|----|----------|------------|------|----------|----------|------------|-----------|----------|--------|
| F1 | high | n/a | unverifiable | security | unverifiable | high | ADR-004 requires per-tenant authorization; no enforcement point found in the API layer | `docs/adr/004-tenancy.md` §Decision; `src/api/` | §6 |
| F2 | medium | n/a | doc-gap | requirements | confirmed | high | No latency or availability target stated for the export feature | `docs/features/export.md` | §5 |
| F3 | low | medium | design-defect | maintainability | risk | medium | `ReportService` imports from the web layer, reversing the dependency direction | `src/services/report.ts:12` | §10 |

Recommendations and remediation plan rows:

| Phase | ID | Findings | Action and benefit | Owner (suggested) | Effort | Depends on | Verification |
|-------|----|----------|--------|-------------------|--------|------------|--------------|
| Now | R1 | F1 | Identify the tenant check in the API layer and document it in ADR-004, or add it if absent | Backend lead | M | none | Test that a cross-tenant request returns 403 |
| Next | R2 | F2 | Add latency and availability targets to the export spec | Product owner | S | none | Targets appear in `export.md` with a verification method |

## Saving

After the report, offer to save it as a Markdown file (suggest `architecture-review.md` in the repository root, or a path of the user's choice), and offer the findings file described in `references/findings-schema.md`. Write only after the user confirms. In a non-interactive run, end the report with the offer as a plain sentence and do not write.
