# Response — eval-3 / without_skill / run-3

**Prompt:** In `deployment.c4`, I was about to add `Prod.Web.webApp -[https]-> Prod.App.apiApp` and `Prod.App.apiApp -[tcp]-> Prod.Data.dbApp` so the diagram shows protocols and ports. Is that the right place, or should those technologies live somewhere else?

---

## Placement of Technologies

The deployment block is **not** the right place for application-level protocol details. Technologies live in the logical model.

### Correct Pattern

```likec4
model {
  // Application-level with protocol as technology
  webApp -[calls]-> apiApp 'Opens session' {
    technology 'HTTPS / REST'
  }
  apiApp -[reads]-> dbApp 'Fetches document' {
    technology 'TCP / MongoDB wire'
  }
}
```

The deployment block (`deployment {}`) is reserved for:
- Infrastructure-specific connections (monitoring, backup, load balancing)
- Relationships that do not exist in the logical model at all

### Why Not in Deployment

The two relationships you proposed duplicate what `instanceOf` already propagates from the logical model. If you add `Prod.Web.webApp -[https]-> Prod.App.apiApp` in deployment, you get duplicate edges in the architecture diagram — which confuses readers.

### Action

1. Add the logical model relationships with `technology` as shown above.
2. Remove (or do not add) the deployment-only versions.
3. The deployment view will show the relationships via `instanceOf` propagation automatically.
