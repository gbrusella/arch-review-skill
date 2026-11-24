# arch-review

A skill that reviews the architecture of a **medium-small application** from its source code and documentation, and reports what is risky, what is unverified, and what to fix first.

It is an application reviewer, not a solution reviewer: it looks at one codebase (and the infrastructure and pipeline files that ship with it), not at a landscape of systems or an enterprise architecture.

The review is read-only. It never changes the project, and it never prints secret values.

## What it checks

- **Design decisions:** ADRs against the MADR format, and the code against what the ADRs and design documents say. A conflict between code and a documented decision is reported as a finding with both citations.
- **Quality attributes:** performance and scalability, resilience, maintainability, observability, data architecture, cost, testing, security (secrets handling and OWASP-style hygiene), supply chain, and auditability.
- **Deployment strategy:** what is documented against what the pipeline actually does (environments, release strategy, rollback, migrations, infrastructure as code).
- **Cloud alignment:** detects the provider from the repository (Azure, AWS, Google Cloud, Oracle Cloud) and rates the project against the provider's well-architected pillars. This is an evidence-based check, not a formal Well-Architected Review.
- **Scenarios:** walks a few concrete failures through the design (a dependency down, a bad deploy, lost backups, 10x load) and records what happens.

## What you get

A report with a verdict (`Not ready`, `Ready with conditions` or `Ready`), the top three actions, a quality-attribute heatmap, strengths, a prioritised findings table, and a remediation plan with an owner role, effort and a verification step for every item.

Every finding carries:

| Field | Meaning |
|---|---|
| Evidence status | `confirmed`, `risk`, `unverifiable` or `assumption`: how you know |
| Severity | Impact if it happens, judged against the system's priorities |
| Likelihood | How likely it is in the target context |
| Confidence | How sure the reviewer is that the finding is correct |
| Category | Security, resilience, performance, and so on |

Missing information is never treated as a pass. If a documented or expected requirement cannot be checked, it is reported as `unverifiable`.

### Depth

- **Compact** (default for small targets: a single ADR, a feature, or roughly 30 source files or fewer): summary, findings, scenarios, one merged plan.
- **Full:** every applicable section, with a minimum amount of source to read and a list of what was sampled.
- **Quick:** a triage across all quality attributes.
- **Delta:** a pull request or diff checked against the existing ADRs (see `references/delta-review.md`).

## Install

Copy this folder into a skills directory so that `SKILL.md` sits at the top of it, for example:

```
~/.claude/skills/arch-review/
```

Then ask for a review in plain language:

> Review the architecture of this project. Is it ready for production?

> Check this Azure API (Bicep plus GitHub Actions) against the documented deployment process and Azure's recommended practices.

> Review this pull request against our ADRs.

## Layout

```
SKILL.md                      the skill: process, vocabulary, output formats
CHANGELOG.md                  version history, newest first
references/
  checklists/                 one checklist per topic, with an index in README.md
  subagents.md                optional parallel specialists for large repositories
  delta-review.md             reviewing a pull request or diff
  findings-schema.md          optional machine-readable findings file
  frameworks.md               pillar lists and category mapping for cloud frameworks
```

## Versions

Releases are tagged (`v2.6` is the current one). `CHANGELOG.md` lists what changed in each.

## Limits

- It reads files and history. It runs no code, scanners or network audits, so nothing it reports is `measured`, and vulnerability status is always left for the owners to check.
- It cannot see live cloud state, repository settings (branch protection, environment reviewers) or external trackers, and it says so in the report instead of guessing.
- It is not a threat assessment, a compliance determination or a certification.
- It has been tried on a handful of small synthetic projects (Node with Terraform, Bicep and CloudFormation) and one real .NET and Bicep repository, with one run per version. Expect rough edges on stacks it has not seen.
