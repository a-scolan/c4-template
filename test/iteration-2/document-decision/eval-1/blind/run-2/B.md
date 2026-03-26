For this specific change, **generally no ADR is needed**.

This skill is for architecture decisions (technology, boundaries, deployment strategy, long-lived trade-offs). A GitHub Actions workflow modification is usually repository/CI tooling, which is out of ADR scope.

## Practical rule
Create an ADR only if the workflow update introduces a durable architecture constraint (not just pipeline mechanics).

Examples that *might* justify ADR:
- release/deployment strategy change affecting architecture risk profile
- mandatory security/compliance gates that materially shape architecture boundaries

Otherwise, document the workflow change in:
- PR rationale
- engineering changelog
- operations documentation if runtime processes are affected
