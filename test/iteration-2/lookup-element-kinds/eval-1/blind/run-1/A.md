Between an app VM and a database VM in **deployment**, use:

- `sql` when you want to model DB protocol/semantics
- `tcp` when you only want generic transport connectivity
- ❌ `calls` is not a deployment relationship kind in this workspace

In the **logical application model**, valid relationship kinds remain:

- `uses`
- `calls`
- `async`
- `reads`
- `writes`

So:
- `calls` stays valid logically
- `sql`/`tcp` are deployment-level kinds, not logical-model kinds

Workspace verification:
1. `projects/shared/spec-deployment.c4` → relationship kinds include `tcp`, `sql`.
2. `projects/shared/spec-global.c4` → relationship kinds include `calls`, `reads`, `writes`, `uses`, `async`.