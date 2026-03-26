# Response — eval-4 / without_skill / run-2

**Prompt:** Prometheus scrapes my production API VM, but browser/API traffic already exists in the logical model. Which deployment relationships should I add, and which ones should I avoid duplicating?

---

## What to Add vs. What to Avoid

### Add: Prometheus Scraping (Infrastructure-Only)

Prometheus scraping is not part of your application topology — it belongs in deployment:

```likec4
Prod.Monitoring.PrometheusVm -[tcp]-> Prod.App.ApiVm 'Metrics scrape :9090'
```

This is appropriate because the scraping relationship has no counterpart in the logical model (Prometheus is infrastructure, not an application actor).

### Avoid: Redrawing Application Traffic

Browser-to-API and API-to-database traffic already exists in `model {}`. Because each deployed `Node_App` uses `instanceOf`, those logical relationships are automatically visible in deployment views. You do not need — and should not — redeclare them:

```
// Remove these if you have them:
// Prod.Web.webApp -[https]-> Prod.App.apiApp
// Prod.App.apiApp -[sql]-> Prod.Data.dbApp
```

Redeclaring creates duplicate edges that undermine diagram readability.

### Rule of Thumb

Ask: "Does this relationship exist in the logical model?" If yes → do not add it to deployment. If no (it is purely infrastructure) → add it to deployment.
