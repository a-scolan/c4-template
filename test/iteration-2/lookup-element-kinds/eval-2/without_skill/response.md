The exact deployment infrastructure kind is `Infra_Fw`. `Infra_Firewall` is **not** declared in the active workspace.

Two nearby valid kinds from the same deployment taxonomy are:
- `Infra_F5`
- `Infra_Router`

You can verify all three directly in `projects/shared/spec-deployment.c4`, where they are declared as:
- `deploymentNode Infra_Fw`
- `deploymentNode Infra_F5`
- `deploymentNode Infra_Router`

So for a firewall in deployment infrastructure, use `Infra_Fw` exactly.
