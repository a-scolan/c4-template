Do not invent VMs. The shared deployment spec includes Node_Cluster and Node_Container, so an honest hierarchy is Node_Environment -> Zone -> Node_Cluster for the managed Kubernetes layer, then deployed workload nodes underneath it.

Safe pattern:
Node_Environment Prod Production {
  #Production
  Zone AppTier Application Tier { #AppTier
    Node_Cluster k8s Managed Kubernetes Cluster {
      Node_App apiApp { instanceOf platform.api }
      Node_App workerApp { instanceOf platform.worker }
    }
  }
}

If a dependency is a managed external service, model it as Node_SaaS or Node_External instead of a fake VM. For wiring, use instanceOf on the deployed application nodes to point back to the logical containers; that is the repository example pattern. Use Node_Container only if you want extra container-level detail.
