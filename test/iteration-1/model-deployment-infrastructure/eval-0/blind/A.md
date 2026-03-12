Use a strict deployment nesting:

- `Node_Environment` for the environment
- `Zone` for security or network boundaries
- `Node_Vm` for the host layer
- `Node_App` for the deployed runtime instance

So the shape to follow is:

`Environment → Zone → VM → Node_App`

For your document platform, a clean production outline is:

```likec4
deployment {
  Node_Environment Prod 'Production' {
    #Production

    Zone Dmz 'DMZ' {
      Node_Vm gatewayVm 'API Gateway VM' {
        Node_App gatewayApp {
          instanceOf docPlatform.apiGateway
        }
      }
    }

    Zone AppTier 'Application Tier' {
      Node_Vm uploadVm 'Upload Service VM' {
        Node_App uploadApp {
          instanceOf docPlatform.uploadService
        }
      }
    }

    Zone ProcTier 'Processing Tier' {
      Node_Vm workerVm 'Processing Worker VM' {
        Node_App workerApp {
          instanceOf docPlatform.processingWorker
        }
      }
    }

    Zone DataTier 'Data Tier' {
      Node_Vm mongoVm 'MongoDB VM' {
        Node_App mongoApp {
          instanceOf docPlatform.mongoDb
        }
      }
    }
  }
}
```

Use `instanceOf` on each `Node_App` to link the deployment node to the logical container it realizes. That is the normal bridge from deployment to the system model.

Do **not** manually copy normal application relationships into the deployment model. Once `instanceOf` is in place, deployed instances inherit the logical interactions from the system model. Add deployment relationships only for infrastructure-specific exceptions such as monitoring flows, replication, bastion access, or explicit network hops that matter operationally.

Make the zone and VM descriptions rich enough to be useful to operators:

- **Zone description:** purpose, trust boundary, subnet or VLAN, ingress and egress expectations, firewall notes
- **VM description:** hostname, OS, vCPU, RAM, storage, mounted volumes, exposed ports, placement
- **VM network table:** list interfaces with `eth0` first, then `eth1`, `eth2`, and so on

That keeps the deployment view honest and readable: environment first, zones second, VMs third, deployed apps last, with the logical linkage carried by `instanceOf`.
