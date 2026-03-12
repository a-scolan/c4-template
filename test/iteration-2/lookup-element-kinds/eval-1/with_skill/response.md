Use the deployment taxonomy for deployment edges, and the logical-model taxonomy for application behavior — they are **not** interchangeable.

For an app VM talking to a database VM in **deployment**:

- Use `sql` when you want to show a database protocol/DB access link specifically.
- Use `tcp` when you only want to show generic network connectivity at the transport level.
- Do **not** use `calls` on the deployment side.

In the **logical application model**, the valid relationships remain the model kinds from the shared spec:

- `calls`
- `reads`
- `writes`
- `async`
- `uses`

For application-to-database behavior, `reads` and `writes` are usually the clearest logical choices. `calls` is still a valid logical-model relationship in general, but it is less precise than `reads` / `writes` for a datastore.

How to confirm in this workspace:

- `projects/shared/spec-deployment.c4` declares deployment relationships such as `http`, `https`, `tcp`, `nfs`, `amqp`, `sql`, `redis`, `smtp`, `ldap`, `oidc_saml`.
- `projects/shared/spec-global.c4` declares logical-model relationships such as `calls`, `reads`, `writes`, `async`, and `uses`.
- If you have project summary tooling available, cross-check with `read-project-summary` before writing model code.

Short version: deployment edge = `tcp` or `sql`; logical model = `calls` / `reads` / `writes` / `async` / `uses`, depending on the behavior you want to express.