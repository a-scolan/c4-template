Use a tiered deployment under one parent environment, for example `Prod`, and keep each zone single-purpose:

## Recommended tiers

- **Dmz** — Internet-facing edge only.
  - Put the **API gateway** here.
  - Responsibilities: TLS termination, request routing, edge filtering, optional rate limiting.
  - Internet exposure: **HTTPS 443 only**.

- **AppTier** — Synchronous business services.
  - Put your **business services** here.
  - Responsibilities: request handling, validation, orchestration, business rules.
  - Internet exposure: **none**.
  - Accept traffic only from `Dmz`.

- **ProcTier** — Asynchronous processing.
  - Put **RabbitMQ** and the **async worker** here.
  - Responsibilities: queueing, event consumption, background jobs, retry handling.
  - Internet exposure: **none**.
  - Keep workers event-driven; they should consume from the queue rather than be called directly from users.

- **DataTier** — Persistent storage.
  - Put **MongoDB** and **MinIO** here.
  - Responsibilities: metadata persistence, object storage, durable state.
  - Internet exposure: **never**.

- **SecZone** *(recommended here)* — Cross-cutting monitoring and security tooling.
  - Put **monitoring** here.
  - Responsibilities: metrics scraping, dashboards, log aggregation, alerting.
  - Internet exposure: **none**.

## Key network / firewall rules

- `Internet -> Dmz`: allow **443/HTTPS**.
- `Dmz -> AppTier`: allow only the internal app ports required for routed requests.
- `AppTier -> ProcTier`: allow **AMQP 5672** for job publishing to RabbitMQ.
- `AppTier -> DataTier`: allow only required data ports, e.g. **MongoDB 27017** and **MinIO 9000/9001 if applicable**.
- `ProcTier -> DataTier`: allow only the write/read ports needed for worker persistence.
- `SecZone -> all tiers`: allow monitoring scrape / telemetry flows only.
- `DataTier`: no inbound access from the Internet, and no broad east-west access.

## Placement summary

- API gateway → `Dmz`
- Business services → `AppTier`
- RabbitMQ + async worker → `ProcTier`
- MongoDB + MinIO → `DataTier`
- Monitoring → `SecZone`

That keeps the deployment readable, secure, and easy to scale by concern rather than by lucky VM sprawl.