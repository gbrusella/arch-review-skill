# Findings file (optional sidecar)

When the user agrees to save the report, also offer `architecture-review.findings.json` next to it. It makes re-review reliable and lets findings be diffed or turned into tickets.

```json
{
  "skill_version": "see CHANGELOG.md",
  "reviewed_at": "YYYY-MM-DD",
  "commit": "<git sha or null>",
  "target": "<path or name>",
  "depth": "quick|full|compact|delta",
  "context": "prototype|production|scale-up",
  "findings": [
    {
      "id": "F1",
      "key": "security/src/api/orders.js/sql-concatenation",
      "severity": "high",
      "likelihood": "high",
      "type": "design-defect",
      "category": "security",
      "evidence": "confirmed",
      "method": "read",
      "confidence": "high",
      "statement": "SQL built by string concatenation with user input",
      "locations": ["src/api/orders.js:7"],
      "status": "open"
    }
  ]
}
```

- `key` is stable across reviews: `<category>/<primary path>/<short-slug>`. Re-review matches on `key`, not on `id`, so renumbering or re-sorting never breaks the link. A moved or renamed file is matched by statement; say so when you do it.
- `method` is `read` (from code or documents) or `measured` (a tool or test was run; name the tool in the report).
- Never put secret values in this file.
