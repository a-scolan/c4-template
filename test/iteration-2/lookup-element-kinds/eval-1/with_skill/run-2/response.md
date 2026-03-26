Between an app VM and a database VM in deployment, use deployment relationship kinds:

- `sql` for DB protocol/data access intent
- `tcp` for generic transport connectivity
- do not use `calls` in deployment edges

In the logical application model, valid relationship kinds are:

- `calls`, `async`, `reads`, `writes`, `uses`

So `calls` remains valid in logical behavior modeling, while `tcp`/`sql` are deployment taxonomy kinds.

Verification sources:

- `projects/shared/spec-global.c4` (logical)
- `projects/shared/spec-deployment.c4` (deployment)