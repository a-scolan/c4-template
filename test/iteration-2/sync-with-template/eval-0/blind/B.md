` .github/skills/create-relationship/SKILL.md` and `projects/shared/spec-context.c4` are the only candidates for an upstream push. They live in the reusable workspace surfaces (`.github` and `projects/shared`), so they are potentially syncable.

These must stay local:
- `projects/payments/system-model.c4`
- `README.md`

Why they stay local:
- `projects/payments/system-model.c4` is a project model under `projects/<project>/`, so it is repository-specific.
- `README.md` is typically local documentation for this repo, not a shared workspace asset.

Before pushing anything upstream, do two checks:
1. **Genericity review** — make sure the changes in the skill/spec help multiple derived repositories, not just this payments project.
2. **Confidentiality review** — remove project names, internal system names, customer details, private architecture, employee/team names, and any other local context.

So the safe split is:
- **Can go upstream after review:** `.github/skills/create-relationship/SKILL.md`, `projects/shared/spec-context.c4`
- **Must stay local:** `projects/payments/system-model.c4`, `README.md`

If either “generic” file still contains payments-specific wording or assumptions, generalize it first and keep the local-only details out of the upstream PR.