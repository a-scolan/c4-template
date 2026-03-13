Upstream-safe:
- `.github/skills/create-relationship/SKILL.md`, if the improvement is generic and confidentiality-safe.
- `projects/shared/spec-context.c4`, because `projects/shared/` is a main automation-facing sync surface for reusable specs.
- `README.md` only if the edits are template-wide documentation for this template repo.

Must stay local:
- `projects/payments/system-model.c4`, because a domain model under `projects/<domain>/` is project-specific.
- Any `README.md` edits that describe the payments repo, internal architecture, customer context, local policies, or repo-specific workflow.

Short rule: upstream gets generic template assets (`.github/`, `projects/shared/`, template-wide docs); local repos keep domain models and project-specific docs.
