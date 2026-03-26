A clean production split is:

- `Prod.Dmz` (edge ingress)
- `Prod.AppTier` (synchronous business services)
- `Prod.ProcTier` (RabbitMQ + async workers)
- `Prod.DataTier` (MongoDB + MinIO)
- optional `Prod.SecZone` (monitoring/security telemetry)

### Tier intent and boundaries

- **DMZ**: internet-facing boundary only (gateway/reverse proxy/TLS).
- **AppTier**: request/response business APIs; can publish jobs.
- **ProcTier**: event-driven background processing; no direct public exposure.
- **DataTier**: persistent stores; reachable only from approved internal tiers.
- **SecZone**: observability and audit, separated from core business path.

### Network policy (minimum)

- Allow `Internet -> DMZ :443`.
- Allow `DMZ -> AppTier` on internal API ports.
- Allow `AppTier -> ProcTier :5672` (AMQP publish).
- Allow `AppTier -> DataTier :27017/:9000` when sync data access is needed.
- Allow `ProcTier -> DataTier :27017/:9000` for job results.
- Allow `SecZone -> tiers` for scrape/collection only; no business transit.
- Deny all non-explicit zone-to-zone traffic.

### LikeC4 shape

```likec4
Prod = Environment "Production" {
  Dmz = Zone "DMZ" {}
  AppTier = Zone "Application Tier" {}
  ProcTier = Zone "Processing Tier" {}
  DataTier = Zone "Data Tier" {}
  SecZone = Zone "Security & Monitoring" {}
}

Internet -> Prod.Dmz
Prod.Dmz -> Prod.AppTier
Prod.AppTier -> Prod.ProcTier
Prod.AppTier -> Prod.DataTier
Prod.ProcTier -> Prod.DataTier
Prod.SecZone -> Prod.AppTier
Prod.SecZone -> Prod.ProcTier
Prod.SecZone -> Prod.DataTier
```

This keeps responsibilities explicit, firewalling reviewable, and scaling independent per tier.