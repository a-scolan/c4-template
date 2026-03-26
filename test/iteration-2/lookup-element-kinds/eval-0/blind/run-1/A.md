Use `Container_Api`.

- ✅ Exact valid kind in this workspace: `Container_Api`
- ❌ Not defined: `Container_API`
- ✅ Also valid but generic: `Container`

For relationships toward a database in the **logical model** (non-deployment), the valid relationship taxonomy is:

- `uses`
- `calls`
- `async`
- `reads`
- `writes`

For a database target, prefer:
- `reads` (read operations)
- `writes` (write operations)

How to verify in the active workspace:
1. Open `projects/shared/spec-containers.c4` and confirm `element Container_Api` exists.
2. In the same file, verify there is no `element Container_API`.
3. Open `projects/shared/spec-global.c4` and check the `relationship` declarations (`uses`, `calls`, `async`, `reads`, `writes`).
4. Open `projects/shared/spec-deployment.c4` to confirm protocol relations like `sql` are deployment-level, not logical-model kinds.