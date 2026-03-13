The cleanest answer is usually both, but with a hard separation of concerns.

- Use a Deployment view for `SecZone`, bastion, firewall, production placement, and network boundaries. Model `SecZone` as a `Zone` instance inside a `Node_Environment 'Production'`, then place `Infra_Fw`, a bastion `Node_Vm`, and any service VMs or app instances inside it.
- Add a C2 view only for the dedicated services that have logical behavior worth documenting. Those services should exist as `Container_*` elements in the system model; the firewall and bastion stay deployment-only.
- Connect the two layers with `instanceOf` so the deployment model reuses the C2 containers instead of inventing separate names.

So: deployment-only if `SecZone` is just infrastructure around already-known services; both if the dedicated services are new architectural building blocks. Because you mentioned dedicated services, I would create both and keep the firewall and bastion out of C2.
