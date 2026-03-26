For this platform, use layered deployment zones under `Prod` with explicit trust boundaries:

1. `Dmz` (public edge)
2. `AppTier` (API/business services)
3. `ProcTier` (RabbitMQ + async workers)
4. `DataTier` (MongoDB + MinIO)
5. optional `SecZone` (monitoring/security operations)

## Responsibilities by tier

- **Dmz**: internet ingress only, TLS termination, request routing.
- **AppTier**: synchronous request handling and business orchestration.
- **ProcTier**: asynchronous work execution from queue events.
- **DataTier**: durable state and object persistence, internal-only.
- **SecZone**: centralized telemetry, logging, alerting, audit visibility.

## Network rules to state explicitly

- Ingress: only `443` from Internet to DMZ.
- DMZ can call only approved AppTier endpoints.
- AppTier can publish to ProcTier (`5672`) and access DataTier (`27017`/`9000`) when needed.
- ProcTier can write/read DataTier for job processing outcomes.
- SecZone has controlled monitoring/log paths to all tiers.
- Default-deny between zones except documented flows.

## Example LikeC4 deployment shape

```likec4
Prod = Environment "Production" {
  Dmz = Zone "DMZ" {}
  AppTier = Zone "Application Tier" {}
  ProcTier = Zone "Processing Tier" {}
  DataTier = Zone "Data Tier" {}
  SecZone = Zone "Security & Monitoring" {}
}

Internet -> Prod.Dmz "HTTPS 443"
Prod.Dmz -> Prod.AppTier "routed internal API"
Prod.AppTier -> Prod.ProcTier "AMQP 5672"
Prod.AppTier -> Prod.DataTier "DB/Object access"
Prod.ProcTier -> Prod.DataTier "job result persistence"
Prod.SecZone -> Prod.AppTier "metrics/log collection"
Prod.SecZone -> Prod.ProcTier "metrics/log collection"
Prod.SecZone -> Prod.DataTier "metrics/log collection"
```

This creates coherent ownership, auditable firewall intent, and clean scaling knobs per tier.