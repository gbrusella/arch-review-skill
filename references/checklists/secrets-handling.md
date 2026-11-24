# Secrets handling

Secrets must live outside the repository. Check the working tree and, when git history is available, history.

- Hardcoded credentials, API keys, tokens, private keys, connection strings, or passwords in source, config, tests, fixtures, scripts, CI files, Dockerfiles, and docs.
- Committed `.env`, key, keystore, or credential files; `.gitignore` coverage for them; placeholder-only templates (for example `.env.example`).
- Git history: use the redacted searches in "Inspecting secrets safely" below or a secret scanner if installed. Leaked-then-removed secrets still count and need rotation.
- How secrets reach the app at runtime (environment injection, vault, managed identity, CI secret store), who can read them, and whether rotation is documented.
- Secret scanning or pre-commit protection in the repository or CI.

**Never reproduce a secret value in the report.** Cite file and line, name the secret type, and redact the value.
A confirmed leaked secret is `high` severity and the recommendation must include rotation.

### Inspecting secrets safely

Never `cat` a secret-bearing file or run `git log -p` unfiltered. Use redacted views so values never reach the transcript:
- Is the file tracked? `git ls-files --error-unmatch .env` (exit 0 means tracked) and `git check-ignore -v .env` for ignore rules. A tracked secret file is a leak even if never edited.
- Citing: key-value and binary secret files have no meaningful line, so cite the file and the key name (for example `.env` key `PAYCO_KEY`), never the value.
- Key names only: `sed -E 's/=.*/=<redacted>/' .env`
- History presence without content: `git log --oneline --all -- .env` and `git log --all --diff-filter=A --name-only -- '*.env' '*.pem' '*.key'`
- Pattern hits as locations only: `git grep -nIE '(sk_live|AKIA|-----BEGIN [A-Z ]*PRIVATE KEY)' | sed -E 's/(:[0-9]+:).*/\1<redacted>/'`
- A scanner that is already installed (for example `gitleaks` or `trufflehog`) may be run with output redaction enabled.
