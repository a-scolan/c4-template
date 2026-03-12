For this workspace, the clean pattern is: model the production hierarchy with shared deployment kinds, then put the view in `views 'Deployment'` with explicit environment → zones → VMs includes.

```likec4
deployment {
  Node_Environment production 'Production' {
    #Production

    Zone_Vlan dmzTier 'DMZ' {
      #Dmz
      Infra_Fw edgeFirewall 'Edge Firewall'
      Node_Vm webGatewayVm 'Web Gateway VM'
    }

    Zone_Vlan appTier 'Application Tier' {
      #AppTier
      Node_Vm webappVm 'Web Application VM'
      Node_Vm apiVm 'API VM'
    }

    Zone_Vlan dataTier 'Data Tier' {
      #DataTier
      Node_Vm databaseVm 'Database VM'
      Node_Vm objectStorageVm 'Object Storage VM'
    }
  }
}

views 'Deployment' {
  deployment view prod_overview {
    title 'Production Infrastructure'

    include production

    include production.dmzTier
    include production.appTier
    include production.dataTier

    include production.dmzTier.edgeFirewall
    include production.dmzTier.webGatewayVm
    include production.appTier.webappVm
    include production.appTier.apiVm
    include production.dataTier.databaseVm
    include production.dataTier.objectStorageVm

    autoLayout TopBottom
  }
}
```

Why this is aligned with the workspace conventions:
- It uses `views 'Deployment'` with a `deployment view`.
- It uses shared deployment kinds such as `Node_Environment`, `Zone_Vlan`, `Node_Vm`, and `Infra_Fw`.
- It lists the environment, each tier, and each VM explicitly — no `*` or `**` wildcards.
- It stops at VM level, which is the default best practice for an overview deployment view.

I would keep ordinary application traffic (`HTTPS`, `SQL`, `AMQP`, etc.) on the system-model relationships and let deployment inherit that context through `instanceOf`, instead of redrawing normal app traffic as explicit deployment edges.
