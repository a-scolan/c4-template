# Response — eval-1 / without_skill / run-3

**Prompt:** I mainly want to split production into `Dmz`, `AppTier`, `ProcTier`, and `DataTier`, with firewall rules between zones. Should this skill detail that itself, or should I switch to another skill?

---

## Deployment Tier Split

The tier split you describe is standard deployment infrastructure modeling in LikeC4. You do not need to switch to a different skill.

### Define Zones Inside the Environment

```likec4
deployment {
  Prod = Node_Environment 'Production' {
    Dmz      = Zone_Vlan 'DMZ' { }
    AppTier  = Zone_Vlan 'Application Tier' { }
    ProcTier = Zone_Vlan 'Processing Tier' { }
    DataTier = Zone_Vlan 'Data Tier' { }
  }
}
```

Each `Zone_Vlan` represents a network segment. Place `Node_Vm` nodes inside each zone as needed.

### Firewall Rules as Deployment Relationships

Use typed deployment relationship kinds to declare allowed traffic between tiers:

```likec4
Prod.Dmz.ApiVm      -[https]-> Prod.AppTier.ServiceVm   'Route external requests'
Prod.AppTier.ServiceVm -[amqp]-> Prod.ProcTier.QueueVm  'Publish job'
Prod.ProcTier.WorkerVm -[tcp]-> Prod.DataTier.DbVm      'Write processed data'
```

### Continuing

Populate each zone with VMs and `Node_App` children as appropriate. Use `instanceOf` to link each deployed app to its corresponding logical model element.
