Start from `projects/template/`, not from `projects/shared/` or `projects/spec-showcase/`.

1. Copy `projects/template/` to `projects/payments/`.
2. Update the local project metadata in `projects/payments/likec4.config.json`:
   - `name`: `payments`
   - `title`: `Payments`
3. Keep one local config file per project. The minimum config is:

```json
{
  "$schema": "https://likec4.dev/schemas/config.json",
  "name": "payments",
  "title": "Payments",
  "include": { "paths": ["../shared"] },
  "imageAliases": { "@": "../shared/images/" }
}
```

4. Keep the project split minimal:
   - `system-model.c4` for actors, systems, containers, and relationships
   - `system-views.c4` for views

Minimum files to create in `projects/payments/`:
- `likec4.config.json`
- `system-model.c4`
- `system-views.c4`

Optional later:
- `ADR/` if you want project-local decisions

Keep `projects/shared/` only for reusable specs, conventions, and shared assets. Put payments-specific actors, systems, containers, and views in `projects/payments/`.
