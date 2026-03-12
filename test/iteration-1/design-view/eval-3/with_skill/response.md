The cleanest approach is to start with a **Deployment** view for `SecZone`, and add a C2 view only if you later discover a separate logical application concern that cannot be explained well in the infrastructure view.

```likec4
views 'Deployment' {
  deployment view secZone_overview {
    title 'Production SecZone'

    include production
    include production.secZone

    include production.secZone.bastionVm
    include production.secZone.firewallVm
    include production.secZone.secretsVm
    include production.secZone.monitoringVm

    autoLayout LeftRight
  }
}
```

Use that first when the goal is to document the zone, its security boundary, and the dedicated hosts inside it.

Add a `views 'C2'` container view only if you also need to explain a distinct logical system structure, such as which services on those hosts interact with `mySystem`, shared platform APIs, or external systems. Do **not** create a C2 view just because the zone exists.

If the harder problem is how to organize `SecZone` relative to DMZ, app, and data layers or how to structure zone/security-rule boundaries, hand that off to `structure-deployment-tiers`.

If you later want special colors, highlighting, or visual emphasis for the bastion or firewall, hand that off separately to `customize-view`; keep this decision about view type and scope independent from styling.
