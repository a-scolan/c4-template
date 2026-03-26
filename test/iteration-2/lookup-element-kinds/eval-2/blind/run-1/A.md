The exact firewall deployment kind in this workspace is `Infra_Fw`.

- ✅ Exact kind: `Infra_Fw`
- ❌ Reject lookalike: `Infra_Firewall`

Two nearby valid deployment kinds are:

- `Infra_F5`
- `Infra_Router`

Verification path (no guessing):

1. Check declared deployment node kinds in `projects/shared/spec-deployment.c4`.
2. Match exact identifier spelling/casing.
3. Prefer declared kind names over readable English variants.

This avoids false positives like `Infra_Firewall` that look reasonable but are not declared.