Do not create a C2 just for bastion and firewall. Those are infrastructure concerns, so the primary artifact should be a Deployment view.

The cleanest approach is:
- Mandatory: one Deployment view for production `SecZone`.
- Optional: one small C2 view only if the zone also introduces real software/service containers that people need to understand logically.

In other words, model `SecZone` as a deployment zone first, for example `Zone SecZone SecZone { #Production #Deployment #Networking ... }`, then place the bastion, firewall, and dedicated service instances inside it with the deployment node types from the shared spec.

Add a C2 only when those dedicated services are meaningful at the application level, such as a scanning service, admin portal, secrets service, or internal API that other actors/systems use. If the zone is mostly topology and hardening, Deployment alone is cleaner. If it has both topology and reusable service behavior, use both, but keep them clearly separated: C2 for logical service boundaries, Deployment for the actual production placement.
