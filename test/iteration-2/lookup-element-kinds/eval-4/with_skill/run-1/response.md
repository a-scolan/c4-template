In the logical model, a web application talking to an API should use `calls` (or `uses` in broader dependency cases), not `https`.

Recommended logical edge:

- `webapp -[calls]-> api`
- protocol detail goes in technology (e.g., `technology 'HTTPS'`)

`https` becomes valid when modeling deployment/infrastructure relationships (deployment taxonomy), not logical behavior flow.

So:

- Logical model: `calls/async/reads/writes/uses`
- Deployment model: `http/https/tcp/sql/...`

If unsure, verify in:

- `projects/shared/spec-global.c4` for logical relationships
- `projects/shared/spec-deployment.c4` for deployment relationships