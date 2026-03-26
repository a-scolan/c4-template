# Response — eval-3 / without_skill / run-1

**Prompt:** In `deployment.c4`, I was about to add `Prod.Web.webApp -[https]-> Prod.App.apiApp` and `Prod.App.apiApp -[tcp]-> Prod.Data.dbApp` so the diagram shows protocols and ports. Is that the right place, or should those technologies live somewhere else?

---

## Protocols in Deployment vs. Logical Model

**Short answer:** The application traffic (`webApp → apiApp`, `apiApp → dbApp`) should live in the **logical model**, not in the deployment block. Protocols belong as `technology` on logical relationships.

### The Rule

In LikeC4:
- **Logical model** (`model {}`): captures application-level intent. Relationship kinds are `calls`, `reads`, `writes`, `async`, etc. Protocol detail goes in the `technology` field:

```likec4
model {
  webApp -[calls]-> apiApp 'Browser requests' {
    technology 'HTTPS'
  }
  apiApp -[reads]-> dbApp 'Query database' {
    technology 'TCP / MongoDB wire protocol'
  }
}
```

- **Deployment** (`deployment {}`): captures infrastructure-level connectivity that has no equivalent in the logical model. Examples: monitoring agents, backup replication, load balancer health checks.

### What to Do with Your Edges

`Prod.Web.webApp -[https]-> Prod.App.apiApp` **duplicates** the logical relationship and should be **removed** from deployment. Instead, ensure the logical model has `webApp -[calls]-> apiApp { technology 'HTTPS' }`.

`Prod.App.apiApp -[tcp]-> Prod.Data.dbApp` similarly duplicates the application-level data access. Move it to the logical model as `apiApp -[reads]-> dbApp { technology 'TCP' }`.

Deployment views propagate these relationships automatically through `instanceOf`, so you will still see them in deployment diagrams without re-declaring them.Short answer: those two relationships are usually **not** the right thing to duplicate in `deployment.c4`.

If `webApp -> apiApp` and `apiApp -> dbApp` already exist in the logical model, keep protocol/technology (and optionally ports) there as the primary source of truth.

Use deployment relationships only for deployment-specific runtime/infrastructure interactions that are not represented logically, such as:

- monitoring scrape paths
- backup/replication channels
- sidecar/service-mesh control traffic
- node-level admin/control-plane communication

So for your example:

- Keep `HTTPS` and `TCP` on logical relationships
- Avoid manually re-adding the same app-to-app edges in deployment unless there is environment-specific behavior you need to model separately
