Do **not** invent hidden physical VMs if managed Kubernetes does not expose or let you manage them. That would make the deployment model look precise while being fiction in a very expensive suit.

Instead, keep an explicit hierarchy around the **operational boundary you actually control**:

- **Environment**: `Prod`
- **Zone**: for example `AppTier` or another production zone you genuinely use
- **Managed platform node**: a cluster/platform node such as `Node_Cluster`
- **Runtime workloads**: `Node_App` instances for the workloads deployed on that platform

A clean pattern is:

```likec4
Prod = Node_Environment "Production" {
  AppTier = Zone "Application Tier" {
    ProdK8sCluster = Node_Cluster "Managed Kubernetes Cluster" {
      apiApp = Node_App "API" {
        instanceOf docPlatform.api
      }

      uploadApp = Node_App "Upload Service" {
        instanceOf docPlatform.uploadService
      }

      workerApp = Node_App "Processing Worker" {
        instanceOf docPlatform.processingWorker
      }
    }
  }
}
```

That keeps the model honest:

- you still have a clear deployment hierarchy
- you do **not** fabricate physical hosts you cannot see or administer
- you still link every deployed workload back to the logical model through `instanceOf`

For `instanceOf`, point each `Node_App` to the matching logical container FQN from the system model. Once you do that, the deployment instances inherit the logical relationships automatically, so you usually do **not** add normal application-to-application deployment edges by hand.

If you also need to discuss production segmentation, ingress zones, or firewall design around the cluster, that is where **`structure-deployment-tiers`** becomes the right follow-up. Keep this skill focused on an honest deployment structure and correct `instanceOf` wiring.