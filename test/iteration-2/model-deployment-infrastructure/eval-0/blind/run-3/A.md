# Response — eval-0 / without_skill / run-3

**Prompt:** I need to document production deployment for a document platform with an API gateway, an upload service, a processing worker, and MongoDB. Give me the LikeC4 structure to follow for environments, zones, VMs, and Node_App. Also explain how to link deployed apps to the logical model and whether deployment relationships must be copied manually.

---

## LikeC4 Deployment Modeling

Organise infrastructure in a four-level nesting: `Node_Environment` → `Zone_Vlan` (or another zone kind) → `Node_Vm` → `Node_App`.

### Example Structure

```likec4
deployment {
  Prod = Node_Environment 'Production' {

    Web = Zone_Vlan 'DMZ' {
      GwVm = Node_Vm 'prod-gateway-vm' {
        technology 'Kong'
        gwApp = Node_App 'API Gateway' {
          instanceOf docs.api
        }
      }
    }

    Services = Zone_Vlan 'App Tier' {
      UpVm = Node_Vm 'prod-upload-vm' {
        technology 'Node.js'
        upApp = Node_App 'Upload' {
          instanceOf docs.uploadService
        }
      }
      WrkVm = Node_Vm 'prod-worker-vm' {
        technology 'Go'
        wrkApp = Node_App 'Worker' {
          instanceOf docs.processingWorker
        }
      }
    }

    Persistence = Zone_Vlan 'Data Tier' {
      DbVm = Node_Vm 'prod-mongo-vm' {
        technology 'MongoDB'
        mongoApp = Node_App 'MongoDB' {
          instanceOf docs.database
        }
      }
    }
  }
}
```

### `instanceOf` Wiring

`instanceOf <fqn>` connects the deployed app to its logical element. The FQN (e.g., `docs.api`) must reference an element declared in your `model {}` block.

### Deployment Relationships

You do **not** need to manually re-declare application relationships from `model {}`. The `instanceOf` binding propagates them to deployment views automatically.

Only add explicit deployment relationships for infrastructure-level connections that have no logical equivalent:

```likec4
Prod.Services.UpVm -[amqp]-> Prod.Services.WrkVm 'Enqueue processing job'
Prod.Services.WrkVm -[tcp]-> Prod.Persistence.DbVm 'Write result to MongoDB'
```

Do not duplicate relationships that are already modelled as `calls`, `async`, or `reads` in the logical model.
