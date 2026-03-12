Use `calls` in the logical model.

For `mySystem.webapp` talking to `mySystem.api`, `https` is not the logical-model relationship kind. In this repository, the model relationship kinds are declared in `projects/shared/spec-global.c4`, and the right choice for this interaction is a model kind such as `calls`.

If the interaction is over HTTPS, put that in the relationship `technology` field, for example as `HTTPS`, while keeping the model kind as `calls`.

`https` becomes valid in this repository only in the deployment taxonomy, where deployment-side infrastructure relationships are declared in `projects/shared/spec-deployment.c4`.

How to confirm it:

1. Check `projects/shared/spec-global.c4` for logical-model relationship kinds such as `calls`.
2. Check `projects/shared/spec-deployment.c4` for deployment relationship kinds such as `https`.
3. If MCP is available, `read-project-summary` can confirm the active taxonomy.
