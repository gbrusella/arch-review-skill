# Maintainability and evolvability

- **Structure:** dependency cycles, layer violations, god classes or modules, shared "utils" or "common" dumping grounds.
- **Hotspots:** files with high churn and high complexity (from repository history); cite the evidence.
- **Duplication:** duplicated domain logic, parallel implementations of one concept, configuration sprawl.
- **Flags and dead code:** long-lived feature flags, unused code paths, stale TODOs.
- **Dependency health:** abandoned or single-maintainer libraries, major-version lag, how upgrades happen and who owns them.
- **Onboarding:** README works as written, local run is possible, conventions are written down, build is reproducible.
- **Reversibility:** lock-in points and the rough cost of replacing each major dependency or vendor.
