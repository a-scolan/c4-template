Keep the deployment modeling scope focused on the infrastructure skeleton, and treat the tier split as a separate `structure-deployment-tiers` concern.

For this deployment framing, the base hierarchy should still stay:

- `Node_Environment`
- `Zone`
- `Node_Vm`
- `Node_App`

So yes, production can absolutely be organized into `Dmz`, `AppTier`, `ProcTier`, and `DataTier`, but the main job here is to keep the deployment hierarchy clean and honest:

- environment boundary at the top
- zones for security/network segmentation
- VMs for operated hosts
- `Node_App` instances inside those VMs, each wired with `instanceOf`

The detailed tier design work—especially firewall rules, allowed paths between zones, and which services belong in which tier—belongs in a dedicated `structure-deployment-tiers` pass. That is where you should decide things like:

- what can talk from `Dmz` to `AppTier`
- whether `ProcTier` is isolated from direct internet ingress
- how `DataTier` is protected
- what firewall rules or ACLs need to be documented between zones

So the short answer is:

- use this deployment framing to establish the infrastructure model
- use `structure-deployment-tiers` for the deeper tier organization and firewall-rule structure

That keeps the work honest and avoids turning one response into a one-stop network design method. This framing gives you the deployment scaffolding; it does not try to fully design the entire security architecture in one go.