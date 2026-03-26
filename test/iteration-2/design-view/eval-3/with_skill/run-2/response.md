Cleanest approach: **both** (C2 + Deployment), each for a different concern.

- **C2 view**: documents the logical boundary and interactions (who talks to which services).
- **Deployment view**: documents where `SecZone` runs (bastion, firewall, dedicated service VMs).

Do not pick only one if you want both architecture clarity and operability.

```likec4
views 'C2' {
  view c2_security_boundary {
    title 'Security-Relevant Container Context'
    include operator
    include corePlatform
    include corePlatform.*
    include externalIdentityProvider
    include -> corePlatform
    include corePlatform ->
  }
}

views 'Deployment' {
  deployment view production_secZone {
    title 'Production SecZone Topology'

    include production
    include production.secZone

    include production.secZone.bastionVm
    include production.secZone.firewallVm
    include production.secZone.authServiceVm
    include production.secZone.auditServiceVm
  }
}
```

Rule of thumb: keep logical app traffic in the model/C2; let deployment inherit it through `instanceOf` instead of redrawing every logical edge in deployment.