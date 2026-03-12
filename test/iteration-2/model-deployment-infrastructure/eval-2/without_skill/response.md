Do not invent physical VMs if the platform does not expose them. If production runs on managed Kubernetes and the underlying hosts are abstracted away, the honest model is to show the deployment nodes you actually know and operate.

A good pattern is:

- `Node_Environment` for `Prod`
- `Zone` for the relevant network/security area
- `Node_Cluster` for the managed Kubernetes cluster or worker pool
- `Node_App` for each deployed workload instance

For example:

```likec4
deployment {
  Node_Environment Prod 'Production' {
    #Production #Infrastructure #Deployment

    Zone AppTier 'Application Tier' {
      Node_Cluster prodK8s 'Managed Kubernetes Cluster' {
        description 'Provider-managed cluster; underlying VM topology is intentionally not modeled.'

        Node_App gatewayApp 'API Gateway Deployment' {
          instanceOf docPlatform.apiGateway
        }

        Node_App uploadApp 'Upload Service Deployment' {
          instanceOf docPlatform.uploadService
        }
      }
    }

    Zone ProcTier 'Processing Tier' {
      Node_Cluster workerPool 'Processing Worker Pool' {
        Node_App workerApp 'Processing Worker Deployment' {
          instanceOf docPlatform.processingWorker
        }
      }
    }

    Zone DataTier 'Data Tier' {
      Node_App mongoApp 'Managed MongoDB' {
        instanceOf docPlatform.mongoDb
      }
    }
  }
}
```

That keeps the hierarchy explicit without making up hidden infrastructure.

How to wire `instanceOf`:

- model the logical containers first (`apiGateway`, `uploadService`, `processingWorker`, `mongoDb`)
- for each runtime deployment node that represents that software in production, set `instanceOf` to the logical element
- keep `instanceOf` on the deployed application/service node (`Node_App`)

So:

- `gatewayApp -> instanceOf docPlatform.apiGateway`
- `uploadApp -> instanceOf docPlatform.uploadService`
- `workerApp -> instanceOf docPlatform.processingWorker`
- `mongoApp -> instanceOf docPlatform.mongoDb`

That gives you two big wins:

1. the deployment view stays faithful to what is really known
2. logical relationships are inherited through `instanceOf`, so you do not need to recreate normal app-to-app traffic at deployment level

If the conversation shifts into how to split the cluster across `Dmz`, `AppTier`, `ProcTier`, `DataTier`, or how to capture firewall boundaries between them, treat that as a separate `structure-deployment-tiers` concern. The important part here is: keep the hierarchy explicit, but never fake physical hosts you do not actually control or see.