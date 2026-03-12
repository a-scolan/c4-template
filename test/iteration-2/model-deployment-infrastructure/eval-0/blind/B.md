Use this deployment structure:

- **Environment**: `Prod`
- **Zones**: `Dmz`, `AppTier`, `ProcTier`, `DataTier`
- **Infrastructure nodes inside each zone**: VMs such as `ProdApigwVm`, `ProdUploadVm`, `ProdWorkerVm`, `ProdMongoVm`
- **Runtime nodes inside each VM**: `Node_App` instances for the deployed services

A good LikeC4 skeleton looks like this:

```likec4
Prod = Node_Environment "Production" {
  Dmz = Zone "DMZ" {
    ProdApigwVm = Node_Vm "prod-apigw-vm" {
      apigwApp = Node_App "API Gateway" {
        instanceOf docPlatform.apiGateway
      }
    }
  }

  AppTier = Zone "Application Tier" {
    ProdUploadVm = Node_Vm "prod-upload-vm" {
      uploadApp = Node_App "Upload Service" {
        instanceOf docPlatform.uploadService
      }
    }
  }

  ProcTier = Zone "Processing Tier" {
    ProdWorkerVm = Node_Vm "prod-worker-vm" {
      workerApp = Node_App "Processing Worker" {
        instanceOf docPlatform.processingWorker
      }
    }
  }

  DataTier = Zone "Data Tier" {
    ProdMongoVm = Node_Vm "prod-mongo-vm" {
      mongoApp = Node_App "MongoDB" {
        instanceOf docPlatform.mongoDb
      }
    }
  }
}
```

Two important rules:

1. **Keep the hierarchy strict**: `Environment → Zone → VM → Node_App`.
2. **Use `instanceOf` on every `Node_App`** to point to the logical container in the system model.

For relationships, do **not** manually copy normal application traffic into `deployment.c4`. Once `apigwApp`, `uploadApp`, `workerApp`, and `mongoApp` use `instanceOf`, they inherit the logical relationships from the system model automatically. Put protocol and port details on the **system-model relationship** instead.

Add deployment relationships only for infrastructure-specific cases such as monitoring, backup, replication, bastion access, or other operational hops.

Also give every zone and VM a rich Markdown description:

- **Zones**: VLAN / CIDR / gateway / firewall intent / purpose
- **VMs**: network and runtime specs in a table

For VM tables, put **`eth0` first**, then OS, CPU, RAM, disk, port, monitoring, RTO, and similar operational details.

Example VM description shape:

```likec4
description """
  Upload service host

  | Property | Value |
  |:---------|:------|
  | eth0 | 10.1.0.12/24 |
  | OS | Ubuntu 22.04 LTS |
  | CPU | 2 vCPU |
  | RAM | 4 GB |
  | Port | 3001 |
  | RTO | 5 minutes |
"""
```

That gives you an honest deployment model, clean traceability back to the logical model, and no duplicated edges doing paperwork twice.