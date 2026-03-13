Use a `deployment view` inside `views 'Deployment'`, and keep the includes explicit from environment down to VM. For example:

views 'Deployment' {
  deployment view prod_overview {
    title 'Production Infrastructure'
    include production
    include production.dmzTier
    include production.appTier
    include production.dataTier
    include production.dmzTier.reverseProxyVm
    include production.dmzTier.bastionVm
    include production.appTier.webVm
    include production.appTier.apiVm
    include production.appTier.workerVm
    include production.dataTier.dbVm
  }
}

That matches the workspace convention of named category folders and avoids `*` / `**` wildcards. Keep the parent hierarchy visible, stop at the VM level by default, and let ordinary application traffic come from inherited `instanceOf` relationships from the system model instead of redrawing deployment-only links.
