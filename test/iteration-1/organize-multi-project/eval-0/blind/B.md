Start from `projects/template/`, not `projects/spec-showcase/`. The template already matches the repo’s minimal project shape.

Create `projects/payments/` with these minimum files:

- `likec4.config.json`
- `system-model.c4`
- `system-views.c4`

Keep the project self-contained by giving `projects/payments/likec4.config.json` its own local metadata and the shared include:

- `name`: `payments`
- `title`: `Payments Architecture`
- `include.paths`: `["../shared"]`
- keep the shared image alias from the template, for example `"@": "../shared/images/"`

Then replace the template placeholders in `system-model.c4` and `system-views.c4` with payments-specific elements and views.

Keep `projects/shared/` for reusable specifications and assets only (shared kinds, tags, styles, images). Do **not** move `payments` systems, actors, or containers into `projects/shared/`.

A clean bootstrap flow is:

1. Copy `projects/template/` to `projects/payments/`.
2. Rename the project metadata in `likec4.config.json`.
3. Update `system-model.c4` with the payments actor/system/container names.
4. Update `system-views.c4` to show the payments context and containers.
5. Leave reusable conventions in `projects/shared/`.
