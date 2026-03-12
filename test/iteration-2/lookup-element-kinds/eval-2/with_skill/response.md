The exact firewall deployment kind in this repository is `Infra_Fw`.

Reject `Infra_Firewall` — that readable name is **not** the declared identifier in the shared deployment spec.

Two nearby valid kinds in the same deployment taxonomy are:

- `Infra_F5`
- `Infra_Router`

You can also see other valid deployment-node kinds nearby in the same file, such as `Node_Vm` and `Zone_Subnet`, but the exact firewall kind itself is `Infra_Fw`.

How to verify it safely in the active workspace:

1. Read `projects/shared/spec-deployment.c4`.
2. Look at the declared `deploymentNode` identifiers under the infrastructure section.
3. Confirm the exact spelling before writing any model code.
4. If available, compare against `read-project-summary` for the active project.

So the answer is: use `Infra_Fw`, not `Infra_Firewall`, and nearby valid kinds include `Infra_F5` and `Infra_Router`.