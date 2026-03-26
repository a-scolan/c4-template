Use a **two-axis structure**:

- Axis A (within primary production): clear tier chain + optional cross-cutting security zone
- Axis B (site level): separate DR environment

## In primary production

Keep existing zones readable:
- `Prod.Dmz`
- `Prod.AppTier`
- `Prod.DataTier`
- (add `Prod.ProcTier` if async exists)

Add cross-cutting audit/security as a sibling zone:
- `Prod.SecZone` or `Prod.AuditSecZone`

This zone should collect logs/metrics/audit events, not carry core request traffic.

## For disaster recovery

Create a separate standby environment/site:
- `ProdDr` (or `DrSite`)

Mirror only required zones for failover clarity (often `DataTier` first, optionally `AppTier`/`Dmz` depending on RTO/RPO strategy).

## Relationships to keep explicit

- `Prod.DataTier -> ProdDr.DataTier` for replication/backup
- optional security-state replication (`Prod.SecZone -> ProdDr.SecZone`)

### Compact skeleton

```likec4
Prod = Environment "Primary Prod" {
  Dmz = Zone "DMZ" {}
  AppTier = Zone "Application Tier" {}
  DataTier = Zone "Data Tier" {}
  SecZone = Zone "Audit & Security" {}
}

ProdDr = Environment "Standby DR" {
  DataTier = Zone "DR Data Tier" {}
}

Prod.DataTier -> ProdDr.DataTier "replication"
```

Result: you gain audit/security and DR coverage without blurring the main tier narrative.