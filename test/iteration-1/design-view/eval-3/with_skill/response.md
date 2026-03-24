Default to **one deployment-style view**, not a new C2. A production `SecZone` with bastion, firewall, and security services is primarily infrastructure, so the cleanest approach is a focused view under `views 'Operations'` (or `views 'Deployment'` if you keep all infra together). Add a C2 **only** if those dedicated services are also real logical containers that need structural explanation outside their placement.

```likec4
views 'Operations' {
  deployment view secZone_overview {
    title 'Production Security Zone'
    description 'Bastion, firewall, and dedicated security services in production'

    include production
    include production.secZone

    include production.secZone.bastionVm
    include production.secZone.firewallVm
    include production.secZone.monitoringVm
    include production.secZone.loggingVm
  }
}
```

Use **both** only when there are two distinct concerns to document:
- C2 for logical responsibilities such as `auditService` or `vaultService`
- Deployment/Operations view for where those services run and how the zone is structured

Do not create a C2 just to redraw bastions, firewalls, or zone boundaries.
