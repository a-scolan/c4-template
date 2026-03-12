Deployment and logical modeling use different relationship taxonomies.

For an app VM talking to a database VM **in deployment**:
- Use `sql` when you want to model database access/query traffic.
- `tcp` is also valid if you only want generic transport connectivity.
- Do **not** use `calls` on the deployment side; it is not a deployment relationship kind.

In the **logical application model**, the declared relationship kinds are `uses`, `calls`, `async`, `reads`, and `writes`.
For app-to-database interactions there, `reads` and `writes` are usually the right choices. `calls` belongs to the logical model, but it is not the deployment taxonomy.

To confirm in this workspace:
- `projects/shared/spec-deployment.c4` declares `tcp` and `sql`.
- `projects/shared/spec-global.c4` declares `calls`, `reads`, and `writes`.
- `projects/shared/SPEC_CHEATSHEET.md` summarizes both sides together.
