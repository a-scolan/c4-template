Keep the deployment readable by separating concerns into four main zones and treating observability as a shared concern:

- **Dmz** (`#Dmz`): API gateway and any public ingress components. Responsibility: TLS termination, request filtering, rate limiting, and routing into internal services. Network rule: accept inbound `HTTPS/443` from the internet; allow outbound only to explicitly exposed internal application endpoints.
- **AppTier** (`#AppTier`): business services behind the gateway. Responsibility: authentication/authorization, document APIs, orchestration of synchronous business workflows, and issuing async work requests. Network rule: accept traffic only from `Dmz`; call `ProcTier` and `DataTier` only on required service ports; no direct public ingress.
- **ProcTier** (`#ProcTier`): RabbitMQ plus the async worker. Responsibility: buffering, background processing, document conversion, event-driven jobs, retries, and workload isolation from the request path. Network rule: accept messages only from approved producers in `AppTier`; workers may consume from RabbitMQ and write to data stores; no direct internet access.
- **DataTier** (`#DataTier`): MongoDB and MinIO. Responsibility: metadata persistence, object storage, backup hooks, and replication targets. Network rule: accept only application- and worker-originated traffic on approved DB/object-storage ports; never expose directly to `Dmz` or the internet.

For **monitoring**, keep it as a small shared operational area adjacent to `AppTier`/`ProcTier` rather than forcing it into the request path. If you must collapse to the four-tier model only, place monitoring components under `AppTier` but tag them `#Monitoring #Observability` so they remain visually distinct.

Recommended allowed flows:

1. Internet -> `Dmz` over `HTTPS`
2. `Dmz` -> `AppTier` over internal `HTTPS` or the chosen app port
3. `AppTier` -> RabbitMQ in `ProcTier` over `AMQP`
4. Async worker in `ProcTier` -> MongoDB / MinIO in `DataTier`
5. `AppTier` -> MongoDB / MinIO only where synchronous business reads or object operations are genuinely required
6. Monitoring -> scrape/export endpoints across tiers; avoid using it as a transit path for business traffic

That gives you a clean LikeC4 deployment story: edge in `Dmz`, business logic in `AppTier`, asynchronous execution in `ProcTier`, and persistence in `DataTier`.