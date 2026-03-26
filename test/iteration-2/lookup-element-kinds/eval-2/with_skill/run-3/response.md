Use `Infra_Fw`.

That is the exact declared firewall deployment kind in this workspace.

Also valid nearby kinds include:

- `Infra_F5`
- `Infra_Router`

Reject similar but undeclared names such as `Infra_Firewall`.

Verification is done by checking declared deployment node kinds in `projects/shared/spec-deployment.c4` and matching exact casing/spelling.