Push upstream only the template-grade changes:

- `.github/skills/create-relationship/SKILL.md`
- `projects/shared/spec-context.c4`

Those are the reusable workspace assets, **but only after** you confirm they are still generic enough for the upstream reference repo.

Keep these local to the derived repository:

- `projects/payments/system-model.c4` — project-specific domain model
- `README.md` — repository-specific documentation for this derived repo, so do not include it in the template push

Before anything goes upstream:

1. Generalize the changes so they do not contain project names, customer/domain details, or repo-specific assumptions.
2. Run a confidentiality review on the diff and remove anything sensitive or identifying.
3. Push only the sanitized generic files, ideally from a dedicated `sync/*` branch, not mixed with local project files.

Short version: the skill file and shared spec are candidates for upstream sync; the payments model and README stay local.