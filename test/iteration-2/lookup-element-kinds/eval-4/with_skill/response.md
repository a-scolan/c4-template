For a web application talking to an API in the **logical model**, the relationship kind should be `calls`, not `https`.

`https` is a deployment-side relationship kind in this workspace, not a logical-model relationship kind.

So the logical-model pattern is:

- kind: `calls`
- protocol detail: put `HTTPS` in the relationship `technology` field

Example shape:

- `Container_Webapp` -> `Container_Api` with relationship kind `calls`
- relationship technology = `HTTPS`

Why: `projects/shared/spec-global.c4` declares the logical-model relationships (`calls`, `reads`, `writes`, `async`, `uses`). `projects/shared/spec-deployment.c4` separately declares deployment relationships such as `http`, `https`, `tcp`, and `sql`.

When does `https` become valid? It becomes valid when you are modeling a **deployment-side infrastructure edge** rather than normal application behavior — for example, a deployment connection between nodes/services where you want the infrastructure protocol itself to be the relationship type.

How to verify in the active workspace:

1. Read `projects/shared/spec-global.c4` for logical-model relationships.
2. Read `projects/shared/spec-deployment.c4` for deployment relationships.
3. Optionally compare with `read-project-summary` for the active project before editing.

Short version: logical model = `calls` + `technology 'HTTPS'`; deployment model = `https` when the edge is truly deployment/infrastructure-level.