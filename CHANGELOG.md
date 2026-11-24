# Changelog

Newest first.

## 2.6.2

- Open source readiness, no change to the skill's behaviour: MIT license, security policy, contributing guide and pull request template; `license` set in the plugin manifests.

## 2.6.1

- Packaging only, no change to the skill's behaviour: the skill moved to `skills/arch-review/`, and the repository is now a plugin and marketplace for Claude Code and Copilot CLI (`.claude-plugin/`), Cursor (`.cursor-plugin/`) and Gemini CLI (`gemini-extension.json`).

## 2.6

- Credential severity rule (confirmed versus unconfirmed, config versus committed), merge/split tie-breaker, Compact plan cap raised to about 10 rows, validity check before the Findings table, minimum evidence for Full, detail paragraphs for `high` only in Full, thin sections 4/7/9 collapse, rename-aware churn, checklist skip rule.

## 2.5

- Tracked-`high` rule defined: owner is a role (never a named individual), scheduled means date, release, or enforced gate; people are referred to by role only.

## 2.4

- Checklists read/skipped listed in Scope, never skipped for time; serial fallback without subagents.
- Documentation lookups allowed for provider facts, else `assumption`; gap/partial/aligned/unverifiable defined; no made-up findings for clean pillars.
- Tracked `high` findings with an owner and scheduled step count as conditions; repo's own finding list cited as `repo <id>`.
- `unverifiable` kinds (claimed versus absent); likelihood for batch systems; `not assessed` heatmap rating.
- Full format merges recommendations and remediation; NFR-doc shortcut; churn excludes docs and generated files; Compact detail rule and no-ADR wording fixed.

## 2.3

- Compact caps (detail only for `high`, at most about 8 plan rows), merge rule, fact-versus-consequence rule for evidence, likelihood check, heatmap rating and priority rules, strengths omitted when empty, ADR line in Compact scope, architecture checklist always read.

## 2.2

- Added deployment strategy check and cloud well-architected alignment (`references/checklists/deployment-and-cloud.md`), cloud provider detection, pillar lists, Output subsection and Compact section.

## 2.1

- Added `supply-chain` category, split-findings rule, `risk` rule for unresolved versions, likelihood for `risk`, credential-exposure severity rule, scenario tagging, secrets citation and tracked-file check, consistent non-interactive wording.

## 2.0

- Added performance, observability, data architecture, maintainability, supply chain, and cost checklists; expanded resilience.
- Split checklists into `references/checklists/<topic>.md`; moved subagent rules to `references/subagents.md`.
- Added Confidence, Likelihood, Category; priority quality attributes, target context, scenario pass, heatmap, strengths, top actions.
- Added Compact format for small targets, delta review mode, findings sidecar file, safe secrets inspection recipe, offline rules, framework mapping.

## 1.0

- Initial version.
