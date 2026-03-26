# Response — eval-4 / without_skill / run-3

**Prompt:** Prometheus scrapes my production API VM, but browser/API traffic already exists in the logical model. Which deployment relationships should I add, and which ones should I avoid duplicating?

---

## Deployment Relationships: Prometheus and App Traffic

### Prometheus Scraping: Add to Deployment

Since Prometheus scraping is an infrastructure-level connection not captured in the logical model, it should be declared in `deployment {}`:

```likec4
Prod.Sec.MonitoringVm -[tcp]-> Prod.App.ApiVm 'Prometheus scrape :9090'
```

### Browser/API Traffic: Do Not Redeclare

Browser-to-API and API-to-database traffic lives in `model {}`. If you have:

```likec4
model {
  webApp -[calls]-> api 'Browser requests' { technology 'HTTPS' }
  api -[reads]-> db 'Fetch data'
}
```

Then through `instanceOf`, deployment views already inherit these edges. You do not need to add:
```
// Avoid: duplicates what instanceOf propagates
// Prod.Web.webApp -[https]-> Prod.App.apiApp
```

### Why This Matters

Duplicate deployment edges appear as two separate arrows on the same diagram — one propagated from the logical model and one you added manually. This makes the deployment view noisy and misleading.

### Summary

- Prometheus scrape → add in deployment (no logical equivalent)
- App-level browser/API traffic → let `instanceOf` propagate it from the logical model
