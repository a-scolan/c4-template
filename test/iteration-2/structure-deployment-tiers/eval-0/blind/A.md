Use four main deployment tiers and keep any operations tooling explicit but secondary:

- `Dmz` — public entry points only: API gateway, reverse proxy, WAF, ingress/load-balancer.
  - Responsibility: terminate external HTTPS, enforce edge security, route traffic inward.
- `AppTier` — business services and synchronous application logic.
  - Responsibility: document workflows, authentication/authorization enforcement, API orchestration.
- `ProcTier` — asynchronous and background execution.
  - Place `RabbitMQ` and the async worker here.
  - Responsibility: queueing, retries, long-running jobs, CPU-heavy processing.
- `DataTier` — persistent state and storage.
  - Place `MongoDB` and `MinIO` here.
  - Responsibility: metadata persistence, object storage, backups/replication.
- Optional `InfraZone` — monitoring/observability stack if you want to avoid mixing it into the business tiers.
  - Responsibility: metrics, logs, tracing, alerting, admin-only access.

Suggested LikeC4 placement summary:

| Tier | Place here |
|---|---|
| `Dmz` | API gateway, reverse proxy, WAF, ingress |
| `AppTier` | Business services, web/API application nodes |
| `ProcTier` | `RabbitMQ`, async worker |
| `DataTier` | `MongoDB`, `MinIO` |
| Optional `InfraZone` | Monitoring, log aggregation, dashboards |

Key network / firewall rules:

1. Internet -> `Dmz` only, typically `HTTPS/443`.
2. `Dmz` -> `AppTier` only on the small set of ingress ports required by the application.
3. `AppTier` -> `ProcTier` for async work submission and control flows (for example `AMQP` to `RabbitMQ`).
4. `ProcTier` -> `DataTier` for persistence and object access; keep this limited to the exact database/storage protocols required.
5. `AppTier` may read/write `DataTier` only when the application truly needs direct persistence access.
6. `DataTier` must have no direct inbound path from the Internet and no direct exposure to `Dmz`.
7. Monitoring should use a dedicated management path into the tiers; it should not become a general transit route for application traffic.
8. Default-deny all other inter-tier traffic and open only the flows you can justify.

A clean mental model is: edge in `Dmz`, business logic in `AppTier`, async execution in `ProcTier`, and persistence in `DataTier`.