# Response — eval-0 / without_skill / run-1

**Prompt:** I need to document production deployment for a document platform with an API gateway, an upload service, a processing worker, and MongoDB. Give me the LikeC4 structure to follow for environments, zones, VMs, and Node_App. Also explain how to link deployed apps to the logical model and whether deployment relationships must be copied manually.

---

## LikeC4 Deployment Structure

The deployment block follows a strict hierarchy: `Node_Environment` → `Zone_*` → `Node_Vm` → `Node_App`.

```likec4
deployment {
  Prod = Node_Environment 'Production' {

    Dmz = Zone_Vlan 'DMZ' {
      ProdApigwVm = Node_Vm 'prod-apigw-vm' {
        technology 'Kong'
        apiApp = Node_App 'API Gateway' {
          instanceOf platform.apiGateway
        }
      }
    }

    App = Zone_Vlan 'Application Tier' {
      ProdUploadVm = Node_Vm 'prod-upload-vm' {
        technology 'Node.js'
        uploadApp = Node_App 'Upload Service' {
          instanceOf platform.uploadService
        }
      }
      ProdWorkerVm = Node_Vm 'prod-worker-vm' {
        technology 'Go'
        workerApp = Node_App 'Processing Worker' {
          instanceOf platform.worker
        }
      }
    }

    Data = Zone_Vlan 'Data Tier' {
      ProdDbVm = Node_Vm 'prod-db-vm' {
        technology 'MongoDB'
        dbApp = Node_App 'MongoDB' {
          instanceOf platform.database
        }
      }
    }
  }
}
```

## Linking to the Logical Model

Use `instanceOf <fqn>` inside each `Node_App` where `<fqn>` is the fully-qualified name of the logical container defined in your `model {}` block. For example, if your model contains:

```likec4
model {
  platform = system 'Document Platform' {
    apiGateway = Container_Api 'API Gateway' { ... }
    uploadService = Container_Service 'Upload Service' { ... }
  }
}
```

Then the deployment node uses `instanceOf platform.apiGateway`, `instanceOf platform.uploadService`, etc.

## Deployment Relationships

Logical model relationships defined with `calls`, `async`, `reads`, etc. are **automatically visible** in deployment views through `instanceOf` binding — you do not need to copy them manually.

However, **infrastructure-only relationships** that have no equivalent in the logical model (VM-to-VM connectivity, monitoring agent scrapes, backup replication) should be added explicitly in the deployment block:

```likec4
Prod.App.ProdUploadVm -[amqp]-> Prod.App.ProdWorkerVm 'Queue jobs'
Prod.App.ProdWorkerVm -[tcp]-> Prod.Data.ProdDbVm 'Write results'
```

Avoid redrawing application traffic (browser to API, API to database) that already exists in the logical model.Use this deployment hierarchy in LikeC4:

- `Prod` (x root)
  - `Dmz` / `AppTier` / `ProcTier` / `DataTier` (zones)
    - VM nodes (when you actually manage/know them)
      - `Node_App` deployed instances (`instanceOf` logical elements)

Example skeleton:

x
model {
  documentPlatform = system 'Document Platform' {
    apiGateway = container 'API Gateway'
    uploadService = container 'Upload Service'
    processingWorker = container 'Processing Worker'
    mongoDb = container 'MongoDB'

    apiGateway -> uploadService 'Routes upload requests' technology 'HTTPS'
    uploadService -> processingWorker 'Enqueues processing jobs'
    processingWorker -> mongoDb 'Stores metadata/results' technology 'TCP'
  }
}

x
  Prod = deploymentNode 'Production' {
    Dmz = deploymentNode 'Dmz' {
      gwVm = deploymentNode 'gw-vm' {
        gwApp = instanceOf documentPlatform.apiGateway
      }
    }

    AppTier = deploymentNode 'AppTier' {
      uploadVm = deploymentNode 'upload-vm' {
        uploadApp = instanceOf documentPlatform.uploadService
      }
    }

    ProcTier = deploymentNode 'ProcTier' {
      workerVm = deploymentNode 'worker-vm' {
        workerApp = instanceOf documentPlatform.processingWorker
      }
    }

    DataTier = deploymentNode 'DataTier' {
      mongoVm = deploymentNode 'mongo-vm' {
        mongoApp = instanceOf documentPlatform.mongoDb
      }
    }
  }
}
```

How linking works:

- `instanceOf` links each deployed runtime node to its logical element.
- Logical relationships are typically reused/implied in deployment views through these links.
- Do **not** manually copy every app-to-app relationship into deployment unless it is deployment-specific (monitoring, firewall, replication, sidecar-only flows, etc.).
