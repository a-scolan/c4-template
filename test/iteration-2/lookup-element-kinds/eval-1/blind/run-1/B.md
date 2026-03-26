In deployment, between an app VM and a database VM, use deployment relationship kinds (`tcp` or `sql`), not `calls`.

- `sql` when the edge represents database protocol/query traffic
- `tcp` when you only model transport connectivity
- `calls` is **not** a deployment relationship kind

In the logical application model, valid kinds remain:

- `calls`
- `async`
- `reads`
- `writes`
- `uses`

So the split is:

- Logical behavior model → `calls/reads/writes/async/uses`
- Deployment infrastructure model → `http/https/tcp/sql/...`

If unsure, verify relationship taxonomies in:

- `projects/shared/spec-global.c4` (logical)
- `projects/shared/spec-deployment.c4` (deployment)