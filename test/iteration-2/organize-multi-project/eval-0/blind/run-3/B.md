Create a new project folder such as `projects/payments/` and keep it structurally aligned with the existing project pattern already visible in this workspace: one local config file, one local model file, one local views file, and an optional local images folder.

Minimum bootstrap:
- `projects/payments/likec4.config.json`
- `projects/payments/system-model.c4`
- `projects/payments/system-views.c4`
- optional `projects/payments/images/`

Keep shared specifications in `projects/shared/` for reusable DSL conventions only: element kinds, tags, relationship kinds, colors, and other workspace-wide modeling rules. In this repository, that shared layer already contains context-level actors/systems and global relationship/tag definitions, so the new project should reference those shared specifications instead of copying them.

A clean bootstrap sequence is:
1. Create `projects/payments/`.
2. Add a local config that includes the shared spec files plus the payments project files.
3. Put only payments-specific business elements and relationships in `system-model.c4`.
4. Put payments-specific views in `system-views.c4`.
5. Add `images/` only if the project needs local icons or aliases.

Rule of thumb: shared = vocabulary and standards; project = actual business model and views. That keeps the new payments project easy to add without leaking project-specific content into the common layer.