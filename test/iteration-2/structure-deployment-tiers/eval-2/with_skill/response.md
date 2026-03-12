Keep the main production tiers readable, and add the cross-cutting pieces explicitly rather than blending them into existing zones.

## Production layout

Keep the primary production environment organized around the main tiers:

- `Dmz` — edge ingress
- `AppTier` — synchronous application services
- `ProcTier` — add this if you have queues, workers, or other async processing
- `DataTier` — databases and storage

If you currently only have `Dmz`, `AppTier`, and `DataTier`, that is fine; add `ProcTier` only when async/runtime processing is a real concern.

## Audit / security zone

Add a separate **`SecZone`** as a sibling tier inside the same production environment.

Use it for things like:
- audit log aggregation
- SIEM / security monitoring
- metrics, dashboards, and alerting
- security scanners or compliance collectors

That keeps security/audit visible without turning `AppTier` or `DataTier` into catch-all zones.

## Standby disaster-recovery site

Model the standby DR site as a **distinct environment**, not as a loose extra box inside the main production tier set.

For example:
- `Prod`
  - `Dmz`
  - `AppTier`
  - `ProcTier` *(if needed)*
  - `DataTier`
  - `SecZone`
- `Dr` or `ProdDr`
  - its own mirrored tier set, or the minimal standby subset you actually operate

This keeps failover topology clear and avoids confusing primary runtime traffic with disaster-recovery infrastructure.

## Readability rules

- Keep `SecZone` explicit and separate; do not use it as a fuzzy replacement for a main tier.
- Keep DR in a separate environment boundary.
- Keep `DataTier` internal-only.
- Keep inter-tier and replication/firewall rules documented explicitly.

For exact VM names, `Node_App` definitions, and `instanceOf` wiring inside those environments, hand off to **`model-deployment-infrastructure`**.