Use this structure and keep it strict:

- `Node_Environment` for `Prod`
- `Zone` nodes inside `Prod`
- `Node_Vm` nodes inside each zone
- `Node_App` nodes inside each VM

For your document platform, a good production layout is:

- `Prod`
  - `Dmz`
    - `ProdApigwVm`
      - `apiGatewayApp`
  - `AppTier`
    - `ProdUploadVm`
      - `uploadApp`
  - `ProcTier`
    - `ProdWorkerVm`
      - `workerApp`
  - `DataTier`
    - `ProdMongoVm`
      - `mongoApp`

Example LikeC4 shape:

```likec4
model {
  Prod = Node_Environment "Production" {
    #Production

    Dmz = Zone "DMZ" {
      description """
        Edge ingress zone

        | Property | Value |
        |:---------|:------|
        | VLAN | 100 |
        | Network | 10.0.0.0/24 |
        | Gateway | 10.0.0.1 |
        | Firewall | Ingress from Internet on 443 |
        | Purpose | API gateway ingress |
      """

      ProdApigwVm = Node_Vm "prod-apigw-vm" {
        description """
          API gateway runtime

          | Property | Value |
          |:---------|:------|
          | eth0 | 10.0.0.10/24 |
          | OS | Ubuntu 22.04 LTS |
          | CPU | 2 vCPU |
          | RAM | 4 GB |
          | Port | 443 |
          | RTO | 5 minutes |
        """

        apiGatewayApp = Node_App "API Gateway" {
          instanceOf documentPlatform.apiGateway
        }
      }
    }

    AppTier = Zone "Application Tier" {
      ProdUploadVm = Node_Vm "prod-upload-vm" {
        uploadApp = Node_App "Upload Service" {
          instanceOf documentPlatform.uploadService
        }
      }
    }

    ProcTier = Zone "Processing Tier" {
      ProdWorkerVm = Node_Vm "prod-worker-vm" {
        workerApp = Node_App "Processing Worker" {
          instanceOf documentPlatform.processingWorker
        }
      }
    }

    DataTier = Zone "Data Tier" {
      ProdMongoVm = Node_Vm "prod-mongo-vm" {
        mongoApp = Node_App "MongoDB" {
          instanceOf documentPlatform.mongoDb
        }
      }
    }
  }
}
```

Use `instanceOf` on every `Node_App` to link the deployed runtime unit back to the logical container in the system model. That link is what makes deployment views inherit the logical relationships.

So no, you generally should **not** copy normal application relationships manually in `deployment.c4`. If `documentPlatform.apiGateway` already calls `documentPlatform.uploadService` in the system model, the deployed instances inherit that relationship automatically. Put protocol and port details on the system-model relationship, not on duplicated deployment edges.

Add deployment relationships only for infrastructure-specific cases such as monitoring agents, backup flows, bastion access, replication, or another operational hop that does not belong in the logical model.

Finally, make the descriptions operationally useful:

- every VM gets a Markdown table
- `eth0` is the first VM row
- include OS, CPU, RAM, disk, port, and RTO on VMs
- include VLAN, CIDR/network, gateway, firewall rules, and purpose on zones