Use this deployment shape as the default skeleton:

1. `Node_Environment` for the environment boundary (`Prod`)
2. `Zone` for network/security areas
3. `Node_Vm` for each host you actually operate
4. `Node_App` inside each VM for each deployed service instance

A clean starting point for your document platform would look like this:

```likec4
deployment {
  Node_Environment Prod 'Production' {
    #Production #Infrastructure #Deployment

    Zone Dmz 'DMZ' {
      description '''
      | Field | Value |
      |---|---|
      | CIDR | 10.10.10.0/24 |
      | Gateway | 10.10.10.1 |
      | Purpose | Internet-facing ingress |
      | Notes | Reverse proxy / edge exposure |
      '''

      Node_Vm gatewayVm 'API Gateway VM' {
        description '''
        | Field | Value |
        |---|---|
        | eth0 | 10.10.10.10/24 |
        | OS | Ubuntu 24.04 |
        | CPU | 4 vCPU |
        | RAM | 8 GB |
        | Disk | 100 GB |
        | Ports | 443 |
        | RTO | 30 min |
        '''

        Node_App gatewayApp 'API Gateway' {
          instanceOf docPlatform.apiGateway
        }
      }
    }

    Zone AppTier 'Application Tier' {
      Node_Vm uploadVm 'Upload VM' {
        Node_App uploadApp 'Upload Service' {
          instanceOf docPlatform.uploadService
        }
      }
    }

    Zone ProcTier 'Processing Tier' {
      Node_Vm workerVm 'Worker VM' {
        Node_App workerApp 'Processing Worker' {
          instanceOf docPlatform.processingWorker
        }
      }
    }

    Zone DataTier 'Data Tier' {
      Node_Vm mongoVm 'MongoDB VM' {
        Node_App mongoApp 'MongoDB' {
          instanceOf docPlatform.mongoDb
        }
      }
    }
  }
}
```

How to link deployment back to the logical model:

- Put the real application/database containers in the logical model first.
- For each deployed runtime instance, add `instanceOf <logical-container>` on the `Node_App`.
- Example: `gatewayApp -> instanceOf docPlatform.apiGateway`, `uploadApp -> instanceOf docPlatform.uploadService`.

Do **not** manually copy normal application relationships into the deployment model. Once `Node_App` instances point to the logical containers with `instanceOf`, they inherit those logical relationships in deployment views. That means the gateway-to-upload-service and worker-to-MongoDB traffic should normally live in the system model, not be duplicated again in `deployment.c4`.

Only add explicit deployment relationships when they describe infrastructure-specific behavior that is not just inherited app traffic—for example replication, monitoring, bastion access, backup transfer, or a very specific network hop.

For descriptions, make them operations-friendly:

- **Zone descriptions:** network purpose, CIDR/subnet, gateway, exposure, firewall posture, routing notes.
- **VM descriptions:** use a Markdown table and put network interfaces first—`eth0` first, then `eth1` if present—followed by OS, CPU, RAM, disk, ports, and recovery/ops details.
- **Avoid redundant hostnames in the table:** the element title already carries that.

So the rule of thumb is simple: **Environment → Zone → VM → Node_App**, with `instanceOf` on `Node_App`, inherited relationships by default, and rich zone/VM descriptions for the operational facts.