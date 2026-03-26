# Response — eval-3 / without_skill / run-2

**Prompt:** In `deployment.c4`, I was about to add `Prod.Web.webApp -[https]-> Prod.App.apiApp` and `Prod.App.apiApp -[tcp]-> Prod.Data.dbApp` so the diagram shows protocols and ports. Is that the right place, or should those technologies live somewhere else?

---

## Where Technologies Belong

Technologies (HTTPS, TCP, etc.) belong on **logical model relationships**, not on deployment edges.

### Logical Model: Correct Placement

```likec4
model {
  webApp -[calls]-> apiApp 'Requests API' {
    technology 'HTTPS'
  }
  apiApp -[reads]-> dbApp 'Queries database' {
    technology 'TCP / MongoDB'
  }
}
```

The relationship **kind** in `model {}` is always a semantic kind (`calls`, `reads`, `async`). The `technology` property carries the protocol detail.

### Deployment: What to Remove

Do **not** add:
```likec4
// Avoid in deployment.c4
Prod.Web.webApp -[https]-> Prod.App.apiApp
Prod.App.apiApp -[tcp]-> Prod.Data.dbApp
```

These are duplicates of logical relationships. Since each `Node_App` uses `instanceOf`, the logical model edges already appear in deployment views without any re-declaration.

### Deployment Edges: What Belongs

Add deployment edges only for infrastructure-only connectivity that does not exist at the application layer:
- Monitoring scrapers (Prometheus → VM)
- Backup replication (storage → backup)
- Load balancer health checks

### Summary

Move HTTPS and TCP technologies to the logical model as `technology` on the relationship. Remove the deployment duplicates.
