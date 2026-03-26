# Response — eval-4 / without_skill / run-1

**Prompt:** Prometheus scrapes my production API VM, but browser/API traffic already exists in the logical model. Which deployment relationships should I add, and which ones should I avoid duplicating?

---

## Deployment Relationships: Add vs. Avoid

### Add: Infrastructure-Only Relationships

Prometheus scraping is a pure infrastructure concern — it does not exist in the logical application model. Add it in `deployment {}`:

```likec4
Prod.SecZone.PrometheusVm -[tcp]-> Prod.App.ApiVm 'Scrape metrics :9090'
```

This is correct because there is no logical model relationship between Prometheus and the API — Prometheus is an operational tool, not an application actor.

### Avoid: Duplicating Logical Relationships

If `webApp -[calls]-> api` already exists in `model {}`, do **not** add it again in deployment:

```
// Do NOT add — this duplicates a logical relationship
// Prod.Web.webApp -[https]-> Prod.App.apiApp
```

The reason: `instanceOf` automatically propagates logical model relationships to deployment views. Adding them again creates duplicate edges and misleads readers about the architecture.

### Decision Table

| Relationship | Already in logical model? | Add to deployment? |
|---|---|---|
| Browser to API (HTTPS) | Yes | No — inherited via `instanceOf` |
| API to Database | Yes | No — inherited via `instanceOf` |
| Prometheus to API VM (scrape) | No | Yes — infrastructure-only |
| Backup agent to Storage VM | No | Yes — infrastructure-only |

### Summary

Only add deployment relationships for infrastructure-specific facts that have no equivalent in the logical model. Everything else is inherited automatically through `instanceOf`.Add deployment relationships for **deployment-only** observability flows, and avoid duplicating core business traffic.

What to add:

- `Prometheus -> API runtime node/VM` (scrape/pull metrics)
- Any other monitoring-only channels that do not exist in logical behavior diagrams

What to avoid duplicating:

- Browser/API traffic already modeled logically
- API/DB business path already modeled logically
- Any app-to-app flow that is already represented by logical relationships and inherited via `instanceOf`

Rule of thumb:

- Logical model = functional/business communication
- Deployment model = runtime/infrastructure-specific communication
