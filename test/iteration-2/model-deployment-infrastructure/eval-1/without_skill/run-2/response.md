# Response — eval-1 / without_skill / run-2

**Prompt:** I mainly want to split production into `Dmz`, `AppTier`, `ProcTier`, and `DataTier`, with firewall rules between zones. Should this skill detail that itself, or should I switch to another skill?

---

## Tier Architecture in LikeC4

Modeling a four-tier production split is a deployment infrastructure task. Define each tier as a `Zone_Vlan` nested inside `Node_Environment`:

```likec4
deployment {
  Prod = Node_Environment 'Production' {
    Dmz     = Zone_Vlan 'DMZ' { }
    AppTier = Zone_Vlan 'Application Tier' { }
    ProcTier = Zone_Vlan 'Processing Tier' { }
    DataTier = Zone_Vlan 'Data Tier' { }
  }
}
```

### Firewall Rules

Document inter-zone connectivity as deployment relationships using protocol-specific kinds:

```likec4
// Internet → DMZ
Prod.Dmz.ApiVm -[https]-> Prod.AppTier.UploadVm 'Route requests'

// AppTier → ProcTier
Prod.AppTier.UploadVm -[amqp]-> Prod.ProcTier.QueueVm 'Enqueue processing'

// AppTier → DataTier
Prod.AppTier.UploadVm -[tcp]-> Prod.DataTier.DbVm 'Query database'

// ProcTier → DataTier
Prod.ProcTier.WorkerVm -[tcp]-> Prod.DataTier.DbVm 'Write results'
```

### What to Do Next

You can continue with this deployment modeling skill to add `Node_Vm` nodes, `Node_App` instances, and `instanceOf` links for each tier. The tier split is core deployment infrastructure and does not require switching to another skill.
