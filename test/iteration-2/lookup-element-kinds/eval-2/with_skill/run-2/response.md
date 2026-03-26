The exact deployment kind for firewall here is `Infra_Fw`.

- ✅ Valid: `Infra_Fw`
- ❌ Invalid lookalike: `Infra_Firewall`

Two nearby valid kinds in the same family:

- `Infra_F5`
- `Infra_Router`

Verification workflow:

1. Read declared deployment node kinds in `projects/shared/spec-deployment.c4`.
2. Match exact identifier spelling and casing.
3. Reject human-friendly variants that are not declared.