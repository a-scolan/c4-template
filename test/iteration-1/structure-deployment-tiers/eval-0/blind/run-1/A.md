Model it as one parent `Production` environment with explicit sibling zones so the hierarchy stays `Environment -> Zone -> VM -> Node_App`.

- `Dmz`: Internet-facing edge tier. Put the API gateway here. Allow `Internet -> Dmz` on HTTPS 443 only, then route internal traffic from `Dmz -> AppTier` on internal HTTP/HTTPS.
- `AppTier`: Synchronous business services only. Put the document platform services here. This tier is internal-only; it receives traffic from `Dmz`, queries `DataTier`, and publishes async work to `ProcTier`.
- `ProcTier`: Async processing tier. Put RabbitMQ and the worker here. `AppTier` publishes jobs/events to RabbitMQ on AMQP 5672; the worker consumes from the queue and persists results. Do not model the worker as directly called from `AppTier`.
- `DataTier`: Persistent storage only. Put MongoDB and MinIO here. This tier is never Internet-facing; allow inbound only from `AppTier` and `ProcTier` on the required data ports.
- `SecZone`: Optional but strongly recommended for monitoring. Put Prometheus/Grafana and log tooling here. Let it scrape metrics from the other tiers and receive logs.

Key network rules:
- Only `Dmz` is Internet-facing.
- `Dmz -> AppTier`: internal request routing.
- `AppTier -> ProcTier`: publish events/jobs, not synchronous worker calls.
- `AppTier -> DataTier`: MongoDB and object-storage access only.
- `ProcTier -> DataTier`: write job results/status.
- `SecZone -> all tiers`: metrics scrape; `AppTier/ProcTier -> SecZone`: log shipping.

Keep each zone single-purpose, document firewall rules in the zone descriptions, and keep every zone explicitly nested under `Production` for clear parent context.
