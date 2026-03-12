For a web application talking to an API in the **logical model**, use the relationship kind `calls`, not `https`.

`HTTPS` belongs in the relationship **technology** field for the logical/system model interaction. In other words, the model kind is `calls`, and the protocol detail is `HTTPS`.

`https` becomes a valid **relationship kind** only on the **deployment/infrastructure** side, where `projects/shared/spec-deployment.c4` declares deployment relationships such as `http`, `https`, `tcp`, and `sql`.

So the split is:
- Logical model: `calls` + technology `HTTPS`
- Deployment model: `https` is valid as a deployment relationship kind between infrastructure/deployment nodes

To confirm, check:
- `projects/shared/spec-global.c4` for logical-model relationships
- `projects/shared/spec-deployment.c4` for deployment relationships
- `projects/shared/SPEC_CHEATSHEET.md` for the summary
