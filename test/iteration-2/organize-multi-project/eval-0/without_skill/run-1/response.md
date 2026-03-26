Add the new project as a thin project shell, and keep the shared area for reusable specifications only.

Minimum bootstrap:

- `projects/payments/likec4.config.json`
- `projects/payments/system-model.c4`
- `projects/payments/system-views.c4`
- optional: `projects/payments/ADR/`

A clean minimal layout is:

- `projects/payments/likec4.config.json` — project config, includes shared specs plus local model/view files
- `projects/payments/system-model.c4` — the actual payments domain model
- `projects/payments/system-views.c4` — views for the payments project

What should go where:

- Shared specs already define reusable building blocks such as tags, relationship kinds, element kinds, deployment nodes, colors, and styles.
- The new business model for payments should live in the new project, not in `projects/shared/`.

Practical bootstrap sequence:

1. Create `projects/payments/`.
2. In `likec4.config.json`, include the shared spec files first, then the local `system-model.c4` and `system-views.c4`.
3. In `system-model.c4`, declare the payments actors/systems/containers using the shared element kinds from `projects/shared/` such as `Actor_*`, `System_*`, `Container_*`, and shared relationships like `calls`, `async`, `reads`, `writes`.
4. In `system-views.c4`, create the project’s context/container/component views.
5. Add ADRs only if you want architecture decisions tracked from day one.

Minimum config idea:

- shared specs included explicitly
- local model and view files included explicitly
- image aliases only if the new project needs its own icons beyond the shared ones

Good default rule: shared = vocabulary and styling, project = owned business model and views. That keeps the new payments project clean and avoids turning shared files into a giant junk drawer.Create a new project folder such as `projects/payments/` and keep it structurally aligned with the existing project pattern already visible in this workspace: one local config file, one local model file, one local views file, and an optional local images folder.

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
Add the new project as a thin project shell, and keep the shared area for reusable specifications only.

Minimum bootstrap:

- `projects/payments/likec4.config.json`
- `projects/payments/system-model.c4`
- `projects/payments/system-views.c4`
- optional: `projects/payments/ADR/`

A clean minimal layout is:

- `projects/payments/likec4.config.json` — project config, includes shared specs plus local model/view files
- `projects/payments/system-model.c4` — the actual payments domain model
- `projects/payments/system-views.c4` — views for the payments project

What should go where:

- Shared specs already define reusable building blocks such as tags, relationship kinds, element kinds, deployment nodes, colors, and styles.
- The new business model for payments should live in the new project, not in `projects/shared/`.

Practical bootstrap sequence:

1. Create `projects/payments/`.
2. In `likec4.config.json`, include the shared spec files first, then the local `system-model.c4` and `system-views.c4`.
3. In `system-model.c4`, declare the payments actors/systems/containers using the shared element kinds from `projects/shared/` such as `Actor_*`, `System_*`, `Container_*`, and shared relationships like `calls`, `async`, `reads`, `writes`.
4. In `system-views.c4`, create the project’s context/container/component views.
5. Add ADRs only if you want architecture decisions tracked from day one.

Minimum config idea:

- shared specs included explicitly
- local model and view files included explicitly
- image aliases only if the new project needs its own icons beyond the shared ones

Good default rule: shared = vocabulary and styling, project = owned business model and views. That keeps the new payments project clean and avoids turning shared files into a giant junk drawer.
For a clean bootstrap, add a **new project folder** (for example `projects/payments/`) and keep it minimal at first:

1. `likec4.config.json`
   - project name/title
   - include paths for model files
   - optional image aliases used by this project
2. `context.c4` (or `model.c4`)
   - define the top-level payments system boundary
3. `containers.c4` (optional but recommended)
   - initial containers and core relationships
4. `views.c4`
   - at least one landscape/context view so the project renders immediately

Minimum practical set is: **config + one model file + one view file**.

Suggested structure:
- `projects/payments/likec4.config.json`
- `projects/payments/model.c4`
- `projects/payments/views.c4`
- `projects/payments/images/` (only if needed)

Keep shared specs read-only from the project perspective (import/include), and keep payments-specific business logic inside `projects/payments/*` so ownership and evolution stay clear.