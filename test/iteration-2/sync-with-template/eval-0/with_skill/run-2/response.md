Classification for upstream sync:

- ✅ **Push upstream**
  - `.github/skills/create-relationship/SKILL.md`
  - `projects/shared/spec-context.c4`

- ❌ **Keep local**
  - `projects/payments/system-model.c4`
  - `README.md`

Reasoning: upstream should contain only reusable workspace assets (`.github/**`, `projects/shared/**`). Files under `projects/<project>/` and root project docs are local context and should not be synced.

Before push: validate genericity + confidentiality, then ensure the sync branch diff contains only intended shared assets.