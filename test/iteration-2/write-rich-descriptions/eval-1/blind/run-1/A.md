For a future `ProdApiVm`, keep the description ops-first and ordered like this:

1. **Role & criticality** — purpose, business impact, tier/environment
2. **Runtime profile** — OS/runtime, CPU/RAM/GPU baseline, expected load
3. **Network surfaces** — interfaces (`eth0`, `eth1`), ingress/egress, key ports/protocols
4. **Dependencies** — DNS, IAM, DB/cache/queue, external services
5. **Observability** — metrics, logs, traces, alert thresholds, dashboards
6. **Reliability controls** — backup, restore target, patching window, failover behavior
7. **Security controls** — hardening, secrets path, access model, audit requirements
8. **Ownership & operations** — owner, on-call, runbooks, escalation path

Do **not** duplicate information already modeled elsewhere:
- Keep relationship technology/protocol details in relationships.
- Keep low-level inventory lists in ops docs/runbooks.
- In the rich description, keep only what operators need to decide and act quickly.