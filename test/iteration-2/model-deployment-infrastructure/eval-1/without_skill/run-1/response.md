# Response — eval-1 / without_skill / run-1

**Prompt:** I mainly want to split production into `Dmz`, `AppTier`, `ProcTier`, and `DataTier`, with firewall rules between zones. Should this skill detail that itself, or should I switch to another skill?

---

## Tier Split in LikeC4

You can model this directly in your deployment file. The four tiers you describe (`Dmz`, `AppTier`, `ProcTier`, `DataTier`) map naturally to LikeC4 zone nodes nested inside a `Node_Environment`.

### Zone Structure

```likec4
deployment {
  Prod = Node_Environment 'Production' {
    Dmz = Zone_Vlan 'DMZ' {
      // API Gateway, Web Server
    }
    AppTier = Zone_Vlan 'Application Tier' {
      // Microservices: Upload, Retrieval
    }
    ProcTier = Zone_Vlan 'Processing Tier' {
      // Message Queue, Workers
    }
    DataTier = Zone_Vlan 'Data Tier' {
      // Database, Object Storage
    }
  }
}
```

### Firewall Rules Between Zones

Add deployment relationships between VM nodes to document network-level connectivity. Use typed relationship kinds to reflect the protocol:

```likec4
// DMZ to AppTier
Prod.Dmz.ApiVm -[https]-> Prod.AppTier.UploadVm 'Route upload requests'

// AppTier to ProcTier (async message publishing)
Prod.AppTier.UploadVm -[amqp]-> Prod.ProcTier.QueueVm 'Enqueue job'

// AppTier to DataTier
Prod.AppTier.UploadVm -[tcp]-> Prod.DataTier.DbVm 'Query metadata'

// ProcTier to DataTier
Prod.ProcTier.WorkerVm -[tcp]-> Prod.DataTier.DbVm 'Write results'
```

### Summary

This is within the scope of deployment infrastructure modeling. You can proceed with defining each zone, adding VMs, and connecting them. For naming conventions and `Node_App` / `instanceOf` wiring, refer to the core deployment hierarchy guidance.You can stay with this deployment-focused workflow.

Your requirement (split `Prod` into `Dmz`, `AppTier`, `ProcTier`, `DataTier` and model firewall boundaries) is exactly deployment infrastructure modeling.

What to include here:

- Deployment hierarchy: `Prod -> zones -> compute/runtime nodes`
- Zone boundaries as deployment nodes
- Explicit firewall/control relationships between zones when they are infrastructure facts
- Clear naming conventions for tiers/zones and gateway points

When to switch:

- Switch only if you need deep network/security policy modeling beyond architecture description (for example full firewall rule tables, IaC generation, or compliance evidence automation).
- For normal LikeC4 architecture deployment diagrams, this is the right place.
