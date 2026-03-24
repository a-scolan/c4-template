Use a `deployment view` in `views 'Deployment'`, ideally in `deployment-views.c4` if the project is split. Follow the workspace convention of explicit includes only: environment first, then each tier, then each VM. No wildcards, and stop at VM level unless placement is the point.

```likec4
views 'Deployment' {
  deployment view production_overview {
    title 'Production Infrastructure'
    description 'DMZ, application tier, and data tier in production'

    include production

    include production.dmzTier
    include production.appTier
    include production.dataTier

    include production.dmzTier.lbVm
    include production.dmzTier.webVm

    include production.appTier.apiVm
    include production.appTier.workerVm

    include production.dataTier.dbVm
    include production.dataTier.cacheVm
  }
}
```

If your hierarchy has clusters inside a tier, include those explicitly between the tier and the VMs.
