`Container_Api` is the exact container kind for the backend API in this workspace. Reject `Container_API` — that spelling is not declared in the shared spec. `Container` is valid, but it is only the generic fallback when no more specific declared subtype fits.

For database interactions in the logical model, the valid relationship taxonomy comes from the shared model spec:

- `calls`
- `reads`
- `writes`
- `async`
- `uses`

For an API talking to a database, `reads` and `writes` are usually the most precise choices. `uses` is acceptable when you intentionally want a broader dependency. Do **not** invent kinds like `query` or `invokes`.

How to verify in the active workspace:

1. Check the active project's `likec4.config.json` to confirm it includes `../shared`.
2. Read `projects/shared/spec-containers.c4` for exact container kinds:
   - `Container_Api`
   - `Container_Database`
3. Read `projects/shared/spec-global.c4` for the logical relationship kinds listed above.
4. If available, compare that against `read-project-summary` for the active LikeC4 project.

So the safe taxonomy is: backend = `Container_Api`, database = `Container_Database`, and the model-side relationships toward the database are `reads` / `writes` (or `uses` when you intentionally stay generic).