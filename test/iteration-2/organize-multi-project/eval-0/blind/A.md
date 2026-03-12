Bootstrap the new project from a **minimal baseline**, not by copying an example project and treating it as the source of truth.

1. Create a new folder such as `projects/payments/`.
2. Add a local `likec4.config.json` owned by the payments project.
3. Keep `include.paths: ["../shared"]` so the project pulls reusable specs through a **relative** path.
4. Create only the minimum useful model files:
   - `system-model.c4`
   - `system-views.c4`
5. Put payments-specific systems, containers, actors, and relationships in those local files.
6. Keep `projects/shared/` for reusable specs, tags, styles, and shared assets only.

A clean starting structure is:
- `projects/payments/likec4.config.json`
- `projects/payments/system-model.c4`
- `projects/payments/system-views.c4`

If you use an existing starter project as a scaffold, keep only the reusable config ideas and remove any example-specific names, systems, and views immediately. That gives you one self-contained project, one config per project, and shared reusable definitions living only in `projects/shared/`.