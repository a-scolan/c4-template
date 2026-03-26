# Response — eval-0 / without_skill / run-2

**Prompt:** I need to document production deployment for a document platform with an API gateway, an upload service, a processing worker, and MongoDB. Give me the LikeC4 structure to follow for environments, zones, VMs, and Node_App. Also explain how to link deployed apps to the logical model and whether deployment relationships must be copied manually.

---

## Deployment Hierarchy in LikeC4

Use the following four-level nesting: `Node_Environment` wraps `Zone_*` which wraps `Node_Vm` which wraps `Node_App`.

```likec4
deployment {
  Prod = Node_Environment 'Production' {

    Dmz = Zone_Vlan 'DMZ' {
      ApiVm = Node_Vm 'prod-apigw-vm' {
        technology 'Kong / Nginx'
        apiApp = Node_App 'API Gateway' {
          instanceOf docPlatform.apiGateway
        }
      }
    }

    AppTier = Zone_Vlan 'Application Tier' {
      UploadVm = Node_Vm 'prod-upload-vm' {
        technology 'Node.js'
        uploadApp = Node_App 'Upload Service' {
          instanceOf docPlatform.uploadService
        }
      }
      WorkerVm = Node_Vm 'prod-worker-vm' {
        technology 'Python'
        workerApp = Node_App 'Processing Worker' {
          instanceOf docPlatform.processingWorker
        }
      }
    }

    DataTier = Zone_Vlan 'Data Tier' {
      DbVm = Node_Vm 'prod-db-vm' {
        technology 'MongoDB 6'
        dbApp = Node_App 'MongoDB' {
          instanceOf docPlatform.documentDb
        }
      }
    }
  }
}
```

## Wiring `instanceOf`

Each `Node_App` declares `instanceOf <fqn>` where `<fqn>` is the FQN from `model {}`. For instance, `docPlatform.apiGateway` means there is an element `apiGateway` nested inside `docPlatform` in your logical model.

## Are Deployment Relationships Required?

Application-level relationships (e.g., upload service calls the database) that already exist in `model {}` are **inherited automatically** through `instanceOf` — no need to duplicate them in `deployment {}`.

You only need to add deployment-level relationships for infrastructure concerns not modelled at the application layer:

- Network-level VM connectivity (`tcp`, `amqp`)
- Monitoring scrapers
- Backup agents

```likec4
Prod.AppTier.UploadVm -[amqp]-> Prod.AppTier.WorkerVm 'Enqueue job'
Prod.AppTier.WorkerVm -[tcp]-> Prod.DataTier.DbVm 'Persist result'
```
