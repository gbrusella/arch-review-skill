# Contributing

Contributions are welcome. All changes go through pull requests; direct pushes to `main` are blocked.

## How to contribute

1. Fork the repository (or create a branch if you have access) and make your change.
2. Open a pull request against `main` and fill in the template.
3. A maintainer will review it. Squash merge is used.

## Guidelines for changes to the skill

- Keep `skills/arch-review/SKILL.md` portable. Its frontmatter has only `name` and `description`, and it should not depend on one tool's features. Optional capabilities (subagents, documentation lookups) must degrade gracefully.
- The review is read-only. Do not add instructions that write to the reviewed project, run installers, or print secret values.
- Do not put real project names, company names, secrets or personal data in examples. Use generic fixtures.
- Keep the skill's wording consistent: the vocabulary in `SKILL.md` is the single definition of evidence status, severity, likelihood, confidence and category.

## Releases

If your change alters the skill or its packaging, add an entry to `CHANGELOG.md` (newest first). The version appears in `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `.cursor-plugin/plugin.json` and `gemini-extension.json`; a maintainer updates all four and tags the release.

## Checks before opening a pull request

- Every JSON manifest is valid.
- If you have Claude Code, `claude plugin validate .` passes.

## License

By contributing you agree that your contribution is licensed under the MIT License in `LICENSE`.
