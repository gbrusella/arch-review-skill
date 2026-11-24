# Supply chain

- Lockfiles committed, versions pinned, a defined update process.
- SBOM or dependency inventory; vulnerability scanning in CI; license review where relevant.
- Build provenance and artifact signing; reproducible builds; registry and mirror configuration (dependency confusion exposure).
- Install-time scripts and vendored code of unknown origin.

### Offline rule

Dependency audit commands that need the network (`npm audit`, `pip-audit`, `osv-scanner` online mode) are not allowed unless the user approves. They may also write lockfiles. If none can run, mark vulnerability status `risk` or `unverifiable` and name the command the owner should run. Do not assert that a version has or has no known advisory from memory.
