# Delta review (PR or diff against the architecture)

Use when the target is a pull request, branch, or diff, not a whole project.

1. Collect the diff and the files it touches. Do not review untouched code except where the change depends on it.
2. Find the ADRs and design documents the changed components fall under. If the change contradicts one, that is a finding citing both the changed lines and the document section. If the change makes a decision obsolete, say the ADR needs updating.
3. Check only the topics the diff can affect (for example a new outbound call: timeouts, retries, idempotency, secrets; a schema change: migration safety, backward compatibility; a new endpoint: authorization, validation, pagination).
4. Check blast radius: callers of changed public symbols, contracts and events consumers rely on, config and feature-flag changes, rollback safety.
5. Check the tests the change adds or should add for each risky path.
6. Output the Compact format (see `SKILL.md`): Summary with verdict, Findings with detail inline, and Recommendations. The verdict applies to merging this change, not to the whole system.
