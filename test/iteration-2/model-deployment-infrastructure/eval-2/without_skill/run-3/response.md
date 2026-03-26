# Response — eval-2 / without_skill / run-3

**Prompt:** I'm deploying on managed Kubernetes in production and I don't have access to underlying VM details. How do I keep an honest deployment hierarchy in LikeC4 without inventing physical hosts? And how do I wire `instanceOf`?

---

## Managed Kubernetes: Honest Hierarchy

The right approach is to represent the Kubernetes cluster as an abstract `Node_Cluster` node and place `Node_App` instances directly inside it, without fabricating physical VMs.

```likec4
deployment {
  Prod = Node_Environment 'Production' {

    KubeProd = Node_Cluster 'prod-cluster' {
      technology 'Google Kubernetes Engine'

      gatewayPod = Node_App 'API Gateway' {
        instanceOf app.apiGateway
      }
      uploadPod = Node_App 'Upload Service' {
        instanceOf app.uploadService
      }
      workerPod = Node_App 'Worker' {
        instanceOf app.worker
      }
      mongoPod = Node_App 'MongoDB' {
        instanceOf app.database
      }
    }

  }
}
```

### Wiring `instanceOf`

Inside each `Node_App`, `instanceOf <fqn>` maps the deployed app to its logical element. The FQN (e.g., `app.apiGateway`) must match the path in `model {}`.

Benefits:
- Propagates logical model relationships to deployment views
- Enables `deploymentView` to show the topology without manually restating relationships
- Keeps the diagram accurate (no fake hosts)

### Summary

Use `Node_Cluster` for managed Kubernetes. Skip `Node_Vm` when you don't have physical node details. Always wire `instanceOf` to maintain the logical–deployment link.
