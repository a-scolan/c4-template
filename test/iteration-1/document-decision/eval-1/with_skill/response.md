Probably not. This skill is for lasting architecture decisions such as technology selection, integration boundaries, deployment strategy, or cross-cutting patterns. A change to a GitHub Actions workflow is repository tooling / CI/CD, which this skill explicitly excludes.

Write an ADR only if the workflow change is a consequence of a deeper architecture decision, for example:
- adopting a new deployment topology or promotion model
- changing rollback or resilience strategy
- introducing a security/compliance boundary that affects the system design

If the change is simply “we updated the workflow file,” then no — this does not need an ADR with this skill.
