Use a **4-core tier chain** and an optional monitoring zone, all nested under `Prod`.

- `Prod.Dmz` (internet edge): API Gateway, optional web server/TLS termination
- `Prod.AppTier` (sync business logic): upload/retrieval/search services
- `Prod.ProcTier` (async processing): RabbitMQ + worker(s)
- `Prod.DataTier` (persistence): MongoDB + MinIO
- `Prod.SecZone` (optional, recommended): Prometheus/Grafana/log pipeline

Keep the main traffic path readable as:

`Internet -> DMZ -> AppTier -> ProcTier -> DataTier`

### Responsibilities

- **DMZ**: only public ingress, TLS termination, request routing, no business state.
- **AppTier**: validates requests, applies business rules, writes metadata, publishes jobs.
- **ProcTier**: consumes queue events asynchronously, performs heavy/background work, writes results.
- **DataTier**: durable storage only; never internet-facing.
- **SecZone**: cross-cutting observability/security telemetry.

### Key network/firewall rules

1. `Internet -> DMZ`: allow `443` only.
2. `DMZ -> AppTier`: allow app/API ports only (e.g. `80/443` internal, or service-specific).
3. `AppTier -> ProcTier`: allow AMQP (`5672`) for publish.
4. `ProcTier -> DataTier`: allow DB/object-storage write paths (`27017`, `9000` as needed).
5. `AppTier -> DataTier`: allow direct sync reads/writes where required (`27017`, `9000`).
6. `SecZone -> all tiers`: allow scrape/pull ports (e.g. `9090`) and controlled log ingest.
7. Deny east-west traffic that is not explicitly required (default deny between zones).

### Minimal LikeC4 deployment skeleton

```likec4
Prod = Environment "Production" {
  Dmz = Zone "DMZ" {}
  AppTier = Zone "Application Tier" {}
  ProcTier = Zone "Processing Tier" {}
  DataTier = Zone "Data Tier" {}
  SecZone = Zone "Security & Monitoring" {}
}

// Typical flows
Internet -> Prod.Dmz
Prod.Dmz -> Prod.AppTier
Prod.AppTier -> Prod.ProcTier
Prod.AppTier -> Prod.DataTier
Prod.ProcTier -> Prod.DataTier
Prod.SecZone -> Prod.AppTier
Prod.SecZone -> Prod.ProcTier
Prod.SecZone -> Prod.DataTier
```

This split gives clear responsibility boundaries, safer firewall policy, and independent scaling per tier.