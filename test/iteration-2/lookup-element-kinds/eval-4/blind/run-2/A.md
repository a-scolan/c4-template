For web app → API in the logical model, use `calls` (not `https`).

`https` is a deployment relationship kind and becomes valid when modeling infrastructure/deployment connectivity.

Practical split:

- Logical model edge: `calls` (technology can still be `HTTPS`)
- Deployment edge: `https`

Taxonomy references in workspace:

- Logical relationships: `projects/shared/spec-global.c4`
- Deployment relationships: `projects/shared/spec-deployment.c4`