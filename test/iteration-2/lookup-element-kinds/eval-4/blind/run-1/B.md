For a web application talking to an API in the **logical model**, use `calls` (or `uses` if you want a generic link).

- ✅ Logical relationship kind: `calls`
- ❌ Logical relationship kind: `https` (not part of logical-model relationship taxonomy)

When `https` becomes valid in this workspace:
- In the **deployment model**, where protocol-level relationships are defined.

Practical modeling rule here:
- Logical model: use `calls` and set relationship technology to `HTTPS` if you want protocol detail.
- Deployment model: use `https` as the relationship kind directly.

Verify in active workspace:
1. `projects/shared/spec-global.c4` → logical kinds (`uses`, `calls`, `async`, `reads`, `writes`).
2. `projects/shared/spec-deployment.c4` → deployment protocol kinds (`http`, `https`, `tcp`, etc.).