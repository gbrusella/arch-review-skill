# Testing and coverage

Applies when the project has executable code.

- **Inventory:** test types present (unit, integration, end-to-end, contract, performance, security), locations, frameworks, how they run locally and in CI.
- **CI gating:** which tests block merge or deploy; skipped, flaky, or quarantined tests; coverage thresholds enforced or not.
- **Coverage data:** state the source, either a coverage report (cite file and date) or a static estimate from reading the code. Never present a static estimate as a measured number.
- **Risk-to-test map:** for each critical path, requirement, or ADR decision (auth, money, data loss, migration, integrations), name the test that covers it or record the gap.
- **Coverage gaps:** untested critical paths, untested error and failure handling, missing boundary and negative cases.
- **Superfluous and redundant tests:** tests that assert the same behavior as another test, test implementation details, assert nothing meaningful, or duplicate fixtures. For each candidate give the test that still covers the behavior and the action (consolidate, rewrite, or delete). Do not recommend deleting a test whose behavior is not covered elsewhere.
