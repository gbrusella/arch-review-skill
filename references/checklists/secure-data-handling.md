# Secure data handling (OWASP Top 10 hygiene)

Review how the code handles data it receives, stores, and emits. Map findings to the OWASP Top 10 category where one fits.

- **Injection (SQL, NoSQL, OS command, LDAP, template):** parameterized queries or safe APIs rather than string concatenation; no user input in shell commands, `eval`, or dynamic queries.
- **Input validation:** server-side validation at trust boundaries (allow-lists, type, length, range); safe file upload and path handling (path traversal); safe deserialization.
- **Output encoding (XSS):** context-appropriate escaping, no raw HTML injection, CSP where relevant.
- **Broken access control:** authorization enforced server-side on every request; object-level checks (IDOR); deny by default.
- **Cryptographic failures:** TLS in transit, encryption at rest for sensitive data, strong password hashing, no custom crypto, no weak algorithms.
- **Authentication and session:** credential storage, session expiry, brute-force protection, MFA where warranted.
- **Insecure design and misconfiguration:** secure defaults, no debug or verbose errors in production, least-privilege service accounts, no default credentials.
- **Vulnerable and outdated components:** dependency pinning, update process, known-vulnerability scanning.
- **Integrity failures:** unsigned updates, untrusted CI/CD inputs, unverified dependencies.
- **Logging and monitoring failures:** security events logged, no sensitive data in logs.
- **SSRF:** server-side requests to user-supplied URLs are restricted.

If the code is not available, record these as `unverifiable` rather than passing them.
