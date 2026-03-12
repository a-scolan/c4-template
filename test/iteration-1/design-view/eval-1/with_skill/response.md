Use a Deployment view and list the hierarchy explicitly from the environment down to each VM.

```likec4
views 'Deployment' {
  deployment view production_overview {
    title 'Production Infrastructure'

    // Environment
    include production

    // Zones
    include production.dmzTier
    include production.appTier
    include production.dataTier

    // DMZ VMs
    include production.dmzTier.bastionVm
    include production.dmzTier.reverseProxyVm
    include production.dmzTier.firewallVm

    // App tier VMs
    include production.appTier.web01Vm
    include production.appTier.web02Vm
    include production.appTier.apiVm
    include production.appTier.workerVm

    // Data tier VMs
    include production.dataTier.postgresVm
    include production.dataTier.redisVm
    include production.dataTier.backupVm

    autoLayout TopBottom
  }
}
```

That matches the repository convention for deployment views: keep the parent hierarchy visible, avoid `*` and `**` wildcards, and stop at VM level rather than drilling into application instances.
