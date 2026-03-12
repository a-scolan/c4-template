Use `calls` for the logical model relationship kind.

In this repository, `https` is not the logical model relationship kind for `mySystem.webapp -> mySystem.api`. The logical relationship taxonomy comes from `projects/shared/spec-global.c4`, and the template example in `projects/template/system-model.c4` shows:

- `mySystem.webapp -[calls]-> mySystem.api`
- with `technology 'HTTPS'`

So the pattern is:

- relationship kind: `calls`
- relationship technology: `HTTPS`

`https` becomes valid as a relationship kind only in deployment/infrastructure modeling, because it is declared in `projects/shared/spec-deployment.c4` alongside other deployment-side relationships such as `http`, `tcp`, and `sql`.

So for this repository:

- logical model: use `calls` and put `HTTPS` in the `technology` field
- deployment model: `https` is valid as a deployment relationship kind
