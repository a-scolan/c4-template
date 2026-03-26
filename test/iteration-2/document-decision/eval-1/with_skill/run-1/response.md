Short answer: **No, usually not with this skill**.

A change to a repository GitHub Actions workflow is typically **tooling/process**, not an architecture decision. Per this skill’s scope, ADRs are for durable architecture choices (technology, boundaries, integration/deployment strategy, cross-cutting design trade-offs).

## When ADR is *not* needed
- Workflow tweaks (lint/test ordering, cache keys, triggers)
- CI ergonomics or speed optimizations
- Repository automation that does not change system architecture

## When ADR *is* justified
Write an ADR only if the workflow change encodes a lasting architecture constraint, for example:
- mandatory security gates tied to production architecture risk posture
- deployment topology or release strategy changes (e.g., blue/green vs rolling) with system-level trade-offs
- compliance requirements that materially affect architecture boundaries

## Better artifact for this specific change
Use:
- PR description + rationale
- `CHANGELOG.md`/engineering log entry
- Ops runbook update (if operational impact exists)

If you want, I can help you draft a lightweight decision note template for CI/CD changes that are important but not ADR-level.
