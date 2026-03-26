Place the new concerns in a way that preserves the primary tier narrative.

## Keep core tiers readable

Primary production path stays:

`Internet -> Dmz -> AppTier -> (ProcTier) -> DataTier`

## Add audit/security as a peer zone

Create `Prod.SecZone` (or `Prod.AuditSecZone`) as a sibling of `Dmz/AppTier/DataTier`.
- It is cross-cutting (metrics, logs, audit events, alerting).
- It should not host core request/processing data paths.

## Add DR as a separate environment/site

Model DR separately, e.g. `ProdDr`:
- `ProdDr.DataTier` for standby replication targets
- optional `ProdDr.AppTier` and `ProdDr.Dmz` depending on failover mode

This avoids cluttering primary production zones with standby infrastructure.

## Explicit cross-environment links

Use dedicated relationships for resilience:
- `Prod.DataTier -> ProdDr.DataTier` (replication/backup)
- optional `Prod.SecZone -> ProdDr.SecZone` for monitoring state replication

### Example skeleton

```likec4
Prod = Environment "Primary Production" {
  Dmz = Zone "DMZ" {}
  AppTier = Zone "Application Tier" {}
  DataTier = Zone "Data Tier" {}
  SecZone = Zone "Audit & Security" {}
}

ProdDr = Environment "Standby DR" {
  DataTier = Zone "DR Data Tier" {}
  AppTier = Zone "DR App Tier" {}
}

Prod.DataTier -> ProdDr.DataTier "replication"
```

Net effect: cross-cutting security is visible, DR is explicit, and tier readability remains intact.