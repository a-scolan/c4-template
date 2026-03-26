Clean bootstrap approach for a new `payments` LikeC4 project:

Create `projects/payments/` with only the minimum baseline:
- `likec4.config.json`
- `system-model.c4`
- `system-views.c4`

Then configure:
1. Unique project identity (`name`, `title`).
2. Shared reuse through relative includes (`include.paths`, e.g. `../shared`).
3. Consistent image aliases with the rest of the workspace.

Modeling scope at day 1:
- Add only payments-owned elements and essential relationships.
- Add only necessary starter views.
- Extend to additional files (deployment/dynamic/etc.) when the project actually needs them.

Anti-patterns to avoid:
- placing payments domain elements in `projects/shared`
- absolute include paths
- inheriting example content unchanged

This yields a clean boundary now and lower maintenance cost later.