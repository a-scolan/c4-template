Use `Infra_Fw`.

- ✅ Exact valid firewall deployment kind: `Infra_Fw`
- ❌ Not defined: `Infra_Firewall`
- ❌ Not defined: alternate spellings like `Infra_FW` or `Infra_FireWall`

Two nearby valid kinds in the same family:
- `Infra_F5`
- `Infra_Router`

How to verify in the active workspace:
1. Open `projects/shared/spec-deployment.c4`.
2. Locate deployment node declarations:
   - `deploymentNode Infra_Fw`
   - `deploymentNode Infra_F5`
   - `deploymentNode Infra_Router`
3. Confirm there is no `deploymentNode Infra_Firewall`.