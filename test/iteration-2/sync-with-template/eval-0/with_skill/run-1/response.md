You can split these files into **upstream-syncable** vs **local-only** like this:

- ✅ **Can be pushed upstream**
  - `.github/skills/create-relationship/SKILL.md` (workspace skill asset)
  - `projects/shared/spec-context.c4` (shared spec asset)

- ❌ **Must stay local**
  - `projects/payments/system-model.c4` (project-specific model under `projects/<project>/`)
  - `README.md` (repo-local documentation/context)

### Why
The upstream reference repo should receive only **reusable workspace assets** (`.github`, `projects/shared`) that are generic across derived repos. Project/domain-specific files (`projects/payments/...`, root docs) stay local.

### Final check before push
1. Genericity: useful outside your payments domain.
2. Confidentiality: no internal architecture, customer names, secrets, employee/team names.
3. Scope: only `.github/**` and/or `projects/shared/**` included in the sync branch diff.