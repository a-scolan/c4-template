Add the Prometheus scrape edge in deployment; avoid duplicating browser/API business traffic.

What to add:

- `ProdMonitoring.prometheusApp -[scrapes]-> ProdApp.ProdApiVm.apiApp`

Why add it: it is infrastructure/operations behavior (observability), not core business interaction.

What to avoid duplicating:

- Browser -> API
- API -> Upload/Worker/DB

If those are already in the logical model, keep them there with technologies and let deployment inherit them via `instanceOf`.