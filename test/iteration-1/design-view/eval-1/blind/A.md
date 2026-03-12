Use a deployment view and enumerate each level explicitly:

```likec4
views 'Deployment' {
  deployment view prod_infrastructure {
    title 'Production Infrastructure'

    include Prod

    include Prod.Dmz
    include Prod.Dmz.firewallVm
    include Prod.Dmz.bastionVm
    include Prod.Dmz.reverseProxyVm

    include Prod.AppTier
    include Prod.AppTier.webVm
    include Prod.AppTier.apiVm

    include Prod.DataTier
    include Prod.DataTier.dbVm
    include Prod.DataTier.cacheVm

    autoLayout TopBottom
  }
}
```

Model the hierarchy as `Node_Environment -> Zone -> Node_Vm`, keep the parent hierarchy visible in the view, avoid `*` or `**`, and stop at VM level unless you want a separate deeper deployment view.
