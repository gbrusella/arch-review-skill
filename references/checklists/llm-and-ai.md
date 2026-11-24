# LLM and AI features

Applies only if the project calls an LLM or ships AI-driven behavior.

Use the OWASP Top 10 for LLM Applications as the reference.

- Prompt injection: untrusted input (user text, documents, web content, tool output) reaching prompts without isolation.
- Output handling: model output executed, rendered, or used in queries without validation.
- Data sent to the model vendor: what is included, whether sensitive or regulated data is sent, vendor retention and training terms.
- Tool and agent permissions: least privilege, human approval for destructive or outward-facing actions.
- Secrets and system prompts: not exposed to users; model API keys handled as secrets.
- Cost and abuse controls: rate limits, token budgets, logging of prompts and responses without leaking sensitive data.
