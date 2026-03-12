Keep the deployment framing here, but push the detailed tier and firewall design into a separate, dedicated pass.

The base hierarchy should still be:

`Environment → Zone → VM → Node_App`

So yes, model `Dmz`, `AppTier`, `ProcTier`, and `DataTier` as zones under production. That is the right level for this infrastructure view.

What I would *not* try to fully solve in the same answer is the detailed security design:

- zone-to-zone firewall matrices
- ingress and egress rule catalogs
- rule ownership and exception handling
- network hardening details per boundary

Use this deployment structure to show **where** workloads run and **which boundary** they sit behind. Handle the full tier-organization and firewall-policy design as a separate network-design step.

In short: this is an infrastructure modeling framework, not an all-in-one answer for complete network and security architecture.
