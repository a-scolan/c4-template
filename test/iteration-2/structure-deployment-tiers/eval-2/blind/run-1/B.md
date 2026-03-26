Add both concerns as **peer zones/environments**, not by overloading existing tiers.

## 1) Cross-cutting audit/security zone

Place it as a sibling zone under production:
- `Prod.SecZone` (or `Prod.AuditSecZone`)

Keep it outside the main business chain so readability remains:

`Internet -> Dmz -> AppTier -> (ProcTier) -> DataTier`

`SecZone` should connect to tiers for telemetry/audit only:
- pulls metrics from App/Proc/Data
- receives logs/events from DMZ/App/Proc
- does not become a transit path for business traffic

## 2) Standby disaster-recovery site

Model DR as a **separate environment/site**, e.g.:
- `ProdDr` (or `DrSite`)

Inside DR, mirror only what is needed for standby clarity:
- `ProdDr.AppTier` (optional warm components)
- `ProdDr.DataTier` (replicas/backup targets)
- optional `ProdDr.Dmz` if active-passive failover includes ingress

## 3) Inter-site links (explicit)

Document cross-site replication as dedicated relationships:
- `Prod.DataTier -> ProdDr.DataTier` (backup/replication)
- optional config/artifact replication from app/ops tooling

Avoid mixing DR nodes directly into the primary `Prod` tier chain; keep them grouped under `ProdDr` for clean mental separation.

### Suggested layout

```likec4
Prod = Environment "Primary Production" {
  Dmz = Zone "DMZ" {}
  AppTier = Zone "Application Tier" {}
  ProcTier = Zone "Processing Tier" {}
  DataTier = Zone "Data Tier" {}
  SecZone = Zone "Audit & Security" {}
}

ProdDr = Environment "Standby DR Site" {
  DataTier = Zone "DR Data Tier" {}
  AppTier = Zone "DR App Tier" {}
}

Prod.DataTier -> ProdDr.DataTier "replication/backup"
```

This preserves tier readability while adding security observability and DR resilience explicitly.