For a production topology, use a **Deployment view** under `views 'Deployment'` with **explicit includes** (no wildcards).

```likec4
views 'Deployment' {
  deployment view production_overview {
    title 'Production Infrastructure'

    // Environment
    include production

    // Zones / tiers
    include production.dmzTier
    include production.appTier
    include production.dataTier

    // VMs (explicit)
    include production.dmzTier.webVm
    include production.dmzTier.edgeFirewallVm
    include production.appTier.apiVm
    include production.appTier.workerVm
    include production.dataTier.dbVm
    include production.dataTier.backupVm
  }
}
```

Why this is aligned: environment first, tier boundaries explicit, each VM listed explicitly, and no deployment wildcards like `production.*`.