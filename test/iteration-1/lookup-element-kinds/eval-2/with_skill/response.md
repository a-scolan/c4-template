The exact kind is `Infra_Fw`.

- `Infra_Fw` is declared in `projects/shared/spec-deployment.c4`.
- `Infra_Firewall` is not declared, so do not use it.

Two nearby valid infrastructure kinds in this repository are:

- `Infra_F5`
- `Infra_Router`

How to verify it:

1. Check `projects/shared/spec-deployment.c4` for the declared `deploymentNode` kinds.
2. If MCP is available, `read-project-summary` can confirm the active deployment taxonomy.
