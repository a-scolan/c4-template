The exact deployment kind for a firewall is `Infra_Fw`.

- `Infra_Fw` is declared in `projects/shared/spec-deployment.c4`.
- `Infra_Firewall` is not declared there, so it is not a valid repository kind.

Two nearby valid kinds from the same deployment infrastructure taxonomy are:

- `Infra_F5`
- `Infra_Router`

You can verify all three directly in `projects/shared/spec-deployment.c4`, where the deployment node declarations are listed verbatim.