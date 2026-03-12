Do not invent physical VMs when managed Kubernetes hides them. Model only the layers that really exist from your operational point of view.

You can still keep an explicit hierarchy, just with honest nodes. For example:

`Environment → Zone → Cluster → Node_App`

That gives you a deployment structure without pretending you own or even know the host layer.

Example:

```likec4
deployment {
  Node_Environment Prod 'Production' {
    #Production

    Zone AppTier 'Application Tier' {
      Node_Cluster k8s 'Managed Kubernetes Cluster' {
        Node_App gatewayApp {
          instanceOf docPlatform.apiGateway
        }
        Node_App uploadApp {
          instanceOf docPlatform.uploadService
        }
        Node_App workerApp {
          instanceOf docPlatform.processingWorker
        }
      }
    }

    Zone DataTier 'Data Tier' {
      Node_App mongoService {
        instanceOf docPlatform.mongoDb
      }
    }
  }
}
```

The rule is simple:

- if the platform exposes a cluster, model the cluster
- if it exposes namespaces, node pools, or a managed database service and those matter, model those layers
- if it does **not** expose VMs, do **not** fabricate `Node_Vm` elements just to satisfy a template

Wire `instanceOf` from each `Node_App` to the logical container it realizes. That is how the deployment model stays connected to the logical model.

As in VM-based deployments, do not manually duplicate normal application relationships in the deployment view. Keep deployment edges for infrastructure-specific cases only. If the discussion shifts toward detailed security zones, tier segmentation, or firewall policies, treat that as a separate network-design step.
