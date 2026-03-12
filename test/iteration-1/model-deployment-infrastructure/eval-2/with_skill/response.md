Do not invent physical VMs if managed Kubernetes hides them. The deployment model should stay honest to the runtime boundary you actually know.

The default pattern of this skill is `Environment → Zone → VM → Node_App`, but in managed infrastructure you should stop at the last real platform boundary that is observable and meaningful. In practice, that usually means:

- `Node_Environment` for `Prod`
- `Zone` for the production runtime boundary
- `Node_Cluster` for the managed Kubernetes cluster or node-pool boundary
- `Node_App` for the deployed workloads

Example:

```likec4
model {
  Prod = Node_Environment "Production" {
    #Production

    AppTier = Zone "Application Tier (managed Kubernetes)" {
      description """
        Managed runtime boundary

        | Property | Value |
        |:---------|:------|
        | Platform | Managed Kubernetes |
        | Exposure | Ingress controller |
        | Ownership | Platform team |
        | RTO | 15 minutes |
      """

      ProdK8sCluster = Node_Cluster "Production Kubernetes Cluster" {
        apiGatewayApp = Node_App "API Gateway" {
          instanceOf documentPlatform.apiGateway
        }

        uploadApp = Node_App "Upload Service" {
          instanceOf documentPlatform.uploadService
        }

        workerApp = Node_App "Processing Worker" {
          instanceOf documentPlatform.processingWorker
        }
      }
    }
  }
}
```

If MongoDB is also managed, model the managed database service honestly as a managed deployment node or service boundary rather than inventing a hidden host.

Wire each workload to the logical model with `instanceOf`, using the full container FQN from the system model. That keeps the deployment view connected to the logical architecture, and relationships between workloads are inherited automatically from the logical model.

For descriptions, document only what is real and operationally useful: cluster purpose, ingress exposure, namespaces, ownership, network expectations, recovery targets, or service class. Do not fabricate host OS, CPU, RAM, or IP rows if those details are abstracted away by the managed platform.

If the discussion turns into DMZ/app/data tier segmentation or firewall rules between zones, hand that part off to `structure-deployment-tiers`.