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

That gives you a clean LikeC4 deployment story: edge in `Dmz`, business logic in `AppTier`, asynchronous execution in `ProcTier`, and persistence in `DataTier`.For this production setup, a clean LikeC4 deployment-tier split could be:

1. **DMZ Tier**
   - **Contains:** API Gateway, edge WAF/reverse proxy, ingress controls.
   - **Responsibilities:** Public entrypoint, TLS termination, coarse request filtering/rate limiting, forwarding to internal app endpoints.
   - **Network rules:**
     - Inbound from Internet to DMZ only (443).
     - DMZ can call App Tier on strictly allowed ports.
     - No direct DMZ access to Data Tier.

2. **Application Tier**
   - **Contains:** Business services, async worker control plane, service-to-service API endpoints.
   - **Responsibilities:** Domain logic, request orchestration, authz enforcement, producing/consuming application events.
   - **Network rules:**
     - Accept traffic only from DMZ and internal trusted subnets.
     - Egress to Processing Tier (RabbitMQ/worker interfaces) and Data Tier through least-privilege rules.
     - No direct inbound from Internet.

3. **Processing Tier** (or Messaging/Proc Tier)
   - **Contains:** RabbitMQ brokers, async worker runtime nodes.
   - **Responsibilities:** Queueing, retry/backoff handling, decoupled asynchronous execution.
   - **Network rules:**
     - RabbitMQ reachable from App Tier producers/consumers on broker ports only.
     - Worker nodes can read queue + call Data Tier or object storage as required.
     - No public ingress.

4. **Data Tier**
   - **Contains:** MongoDB, MinIO.
   - **Responsibilities:** Persistent document metadata/state (MongoDB) and binary object storage (MinIO).
   - **Network rules:**
     - Only reachable from App/Processing tiers.
     - Block lateral access from DMZ.
     - Enforce encryption in transit and role-scoped credentials.

5. **Operations/Observability Tier**
   - **Contains:** Monitoring/metrics/logging/alerting stack.
   - **Responsibilities:** Health telemetry, SLO alerting, operational visibility across all tiers.
   - **Network rules:**
     - Pull/scrape or receive telemetry from internal tiers.
     - Admin access from secured operations network only.
     - No broad east-west trust; explicit allowlists.

### Key cross-tier principles
- **Default-deny networking** between tiers, explicit allow rules only.
- **No Internet-to-App/Data direct path**.
- **Secrets and identity** scoped per service role.
- **Asynchronous isolation**: RabbitMQ/worker failures should not directly collapse synchronous API availability.
- **Observability isolation**: monitoring reads from workloads but should not become an implicit transit path to data systems.