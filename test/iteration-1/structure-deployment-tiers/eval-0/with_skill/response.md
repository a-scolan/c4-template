Use a layered deployment with clear zone boundaries:

## Recommended tiers

- **Dmz** — internet-facing edge only. Place the API gateway here, and optionally a web server or load balancer if they terminate TLS or route traffic.
- **AppTier** — business-facing synchronous services. Place the document vault business services here.
- **ProcTier** — asynchronous processing. Place **RabbitMQ** and the **async worker** here so background execution stays isolated from request/response traffic.
- **DataTier** — persistent storage only. Place **MongoDB** and **MinIO** here.
- **SecZone** *(optional but recommended)* — monitoring and security tooling such as Prometheus, Grafana, log aggregation, or alerting.
- **InfraZone** *(optional)* — backup/DR tooling if you want operational infrastructure separated from the main production flow.

## Responsibilities by tier

- **Dmz**: TLS termination, edge routing, request filtering, minimal exposure to the public internet.
- **AppTier**: validate requests, enforce business rules, orchestrate document workflows, publish async jobs.
- **ProcTier**: receive queued jobs, process background work, update status/results.
- **DataTier**: store metadata in MongoDB and binary objects in MinIO; never host public endpoints.
- **SecZone**: collect metrics/logs and emit alerts without becoming a fuzzy catch-all for application runtime.

## Key network and firewall rules

- **Internet → Dmz**: allow only HTTPS 443.
- **Dmz → AppTier**: allow only the internal application ports needed for routed requests.
- **AppTier → ProcTier**: allow AMQP 5672 (or the broker port you standardize on) for job publishing.
- **AppTier → DataTier**: allow MongoDB 27017 and MinIO/S3 port 9000 only if the business services need direct reads/writes.
- **ProcTier → DataTier**: allow only the database/storage ports needed for worker persistence.
- **SecZone → all tiers**: outbound scraping/collection only for metrics and logs; keep inbound access tightly limited.
- **DataTier**: **no internet exposure** and no direct public ingress.

## Placement guidance

- Keep queue and workers in **ProcTier**, not in AppTier.
- Keep **MongoDB** and **MinIO** together in **DataTier** as persistent stores.
- If the system is strictly synchronous you can omit **ProcTier**, but with RabbitMQ and workers present it should be explicit.