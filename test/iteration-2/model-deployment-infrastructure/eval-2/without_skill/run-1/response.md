# Response — eval-2 / without_skill / run-1

**Prompt:** I'm deploying on managed Kubernetes in production and I don't have access to underlying VM details. How do I keep an honest deployment hierarchy in LikeC4 without inventing physical hosts? And how do I wire `instanceOf`?

---

## Honest Kubernetes Hierarchy in LikeC4

On managed Kubernetes (GKE, EKS, AKS), you typically don't have access to underlying node IDs. Instead of inventing physical VMs, use an abstract cluster node.

### Recommended Approach: Use `Node_Cluster`

```likec4
deployment {
  Prod = Node_Environment 'Production' {
    K8s = Node_Cluster 'Kubernetes Cluster' {
      apiPod = Node_App 'API Gateway' {
        instanceOf platform.apiGateway
      }
      uploadPod = Node_App 'Upload Service' {
        instanceOf platform.uploadService
      }
      workerPod = Node_App 'Processing Worker' {
        instanceOf platform.worker
      }
      dbPod = Node_App 'MongoDB' {
        instanceOf platform.database
      }
    }
  }
}
```

This keeps the hierarchy honest: you represent what you actually know without fabricating host details.

### Wiring `instanceOf`

Each `Node_App` uses `instanceOf <fqn>` referencing a logical element from `model {}`:

```likec4
apiPod = Node_App 'API Gateway' {
  instanceOf platform.apiGateway  // must exist in model {}
}
```

### Optional: Namespace Layer

If Kubernetes namespaces are architecturally significant, add an intermediate `Node_Cluster` node:

```likec4
K8s = Node_Cluster 'Kubernetes Cluster' {
  ProdNs = Node_Cluster 'production' {
    apiPod = Node_App 'API Gateway' {
      instanceOf platform.apiGateway
    }
  }
}
```

Only add this level if the namespace boundary is meaningfully distinct for readers.Great constraint to keep: model what you truly know.

For managed Kubernetes in production, an honest hierarchy is usually:

- `Prod` (environment)
  - managed K8s cluster (provider-managed control plane)
    - namespace or workload grouping nodes
      - deployed app instances (`instanceOf` logical containers/components)

Do **not** invent physical hosts/VMs if they are opaque to your team.

Example pattern:

```likec4
deployment {
  Prod = deploymentNode 'Production' {
    k8s = deploymentNode 'Managed Kubernetes Cluster' {
      apiNs = deploymentNode 'api-namespace' {
        apiPod = instanceOf documentPlatform.apiGateway
      }
      uploadNs = deploymentNode 'upload-namespace' {
        uploadPod = instanceOf documentPlatform.uploadService
      }
      workerNs = deploymentNode 'worker-namespace' {
        workerPod = instanceOf documentPlatform.processingWorker
      }
    }
  }
}
```

`instanceOf` wiring rule:

- Left side = deployed runtime node in deployment model
- Right side = existing logical element id (container/component/system)

So you preserve traceability without fabricating infrastructure detail.
