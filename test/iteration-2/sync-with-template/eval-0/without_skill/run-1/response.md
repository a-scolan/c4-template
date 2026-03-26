You can push only changes that are template-generic and repository-agnostic.

- **Can be pushed upstream (`c4-template`)**
  - `.github/skills/create-relationship/SKILL.md` **if** the improvement is generic (no customer names, no internal URLs, no proprietary process details).
  - `projects/shared/spec-context.c4` **if** it remains reusable for all derived repos (no tenant/business-specific modeling).
  - `README.md` **only if** the edits are for global template usage (setup, workflow, neutral docs).

- **Must stay local**
  - `projects/payments/system-model.c4` (domain/tenant-specific project content).
  - Any `README.md` section that documents local-only conventions, customer context, or private infrastructure.

Quick rule: if a change helps *every* downstream repository and contains no confidential/local context, it is upstream-safe; otherwise keep it local.