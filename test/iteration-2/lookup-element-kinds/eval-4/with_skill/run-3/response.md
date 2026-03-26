Use `calls` for web application → API in the logical model.

`https` is not the logical behavior kind; it is a deployment relationship kind.

When `https` is valid:

- In deployment/infrastructure modeling (`spec-deployment.c4` taxonomy)

Logical/deployment split to keep safe:

- Logical: `calls`, `async`, `reads`, `writes`, `uses`
- Deployment: `http`, `https`, `tcp`, `sql`, etc.

You can still annotate a logical `calls` edge with technology `HTTPS`.