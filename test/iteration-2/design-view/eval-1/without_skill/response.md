Use a deployment view and enumerate each level explicitly.

```likec4
deployment {
  Node_Environment Prod 'Production' {
    #Production

    Zone Dmz 'DMZ' {
      #Dmz
      Node_Vm bastionVm 'Bastion VM'
      Node_Vm edgeProxyVm 'Edge Proxy VM'
    }

    Zone AppTier 'Application Tier' {
      #AppTier
      Node_Vm webVm 'Web VM'
      Node_Vm apiVm 'API VM'
    }

    Zone DataTier 'Data Tier' {
      #DataTier
      Node_Vm dbVm 'Database VM'
    }
  }
}

views 'Deployment' {
  deployment view production_overview {
    title 'Production Infrastructure'

    include Prod
    include Prod.Dmz
    include Prod.Dmz.bastionVm
    include Prod.Dmz.edgeProxyVm
    include Prod.AppTier
    include Prod.AppTier.webVm
    include Prod.AppTier.apiVm
    include Prod.DataTier
    include Prod.DataTier.dbVm
  }
}
```

That matches the workspace conventions:
- explicit hierarchy: environment -> zones -> VMs
- no `*` or `**` wildcards
- parent hierarchy stays visible
- the view stops at VM level

For ordinary application traffic, prefer relationships from the system model and let deployed instances inherit them. Add explicit deployment relationships only when the infrastructure link itself is what you need to document.