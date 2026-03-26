# Response — eval-2 / without_skill / run-2

**Prompt:** I'm deploying on managed Kubernetes in production and I don't have access to underlying VM details. How do I keep an honest deployment hierarchy in LikeC4 without inventing physical hosts? And how do I wire `instanceOf`?

---

## Kubernetes Without Physical VMs

When running managed Kubernetes, it is correct to omit the physical node layer. Model the cluster as a single abstract node and place app instances directly inside it.

### Minimal Honest Structure

```likec4
deployment {
  Prod = Node_Environment 'Production' {
    Cluster = Node_Cluster 'k8s-prod' {
      apigwApp = Node_App 'API Gateway' {
        instanceOf mySystem.apiGateway
      }
      uploadApp = Node_App 'Upload Service' {
        instanceOf mySystem.uploadService
      }
      workerApp = Node_App 'Worker' {
        instanceOf mySystem.worker
      }
      dbApp = Node_App 'MongoDB' {
        instanceOf mySystem.database
      }
    }
  }
}
```

### How `instanceOf` Works

`instanceOf <fqn>` links the deployed pod representation to the logical container. The `<fqn>` must match an element declared in `model {}`. This propagates the logical relationships to deployment views automatically.

### Things to Avoid

- Do **not** invent `Node_Vm 'unknown-node-1'` nodes with fake IPs — this adds inaccurate information.
- Do **not** skip `instanceOf` — you lose the link to the logical model and relationship propagation stops working.
