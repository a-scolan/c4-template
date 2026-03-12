Use the deployment taxonomy between deployment nodes, not the logical-model taxonomy.

Between an app VM and a database VM in deployment:

- `tcp` is valid for a network-level connection.
- `sql` is valid for a database-specific deployment interaction.
- `calls` is not a deployment relationship kind here, so do not use it between deployment nodes.

In the logical application model, the valid model relationship kinds remain:

- `calls`
- `reads`
- `writes`
- `async`
- `uses`

So the two layers do not share the same taxonomy: deployment may use `tcp` or `sql`, while the logical model should use kinds such as `calls`, `reads`, or `writes`.

How to confirm it:

1. Check `projects/shared/spec-deployment.c4` for deployment relationships such as `tcp` and `sql`.
2. Check `projects/shared/spec-global.c4` for logical-model relationships such as `calls`, `reads`, `writes`, `async`, and `uses`.
3. If MCP is available, `read-project-summary` can confirm the active taxonomy.
