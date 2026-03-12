Use a simple four-tier production layout and keep each tier responsible for one kind of exposure or state.

## Recommended tier split

| Tier | Place here | Main responsibility |
| --- | --- | --- |
| `Dmz` | API gateway, public ingress, load balancer or reverse proxy | Terminate external traffic and expose only approved entry points |
| `AppTier` | Business services for the document vault | Handle synchronous application logic and API orchestration |
| `ProcTier` | RabbitMQ, async worker | Run background processing and decouple long-running jobs from request/response paths |
| `DataTier` | MongoDB, MinIO | Store persistent business data and documents |
| `InfraZone` *(optional)* | Monitoring stack, logging, admin tooling | Operate and observe the platform without mixing it into business tiers |
| `SecZone` *(optional)* | Audit, secrets, security scanning, SIEM hooks | Centralize cross-cutting security controls |

## Placement notes

- Put the API gateway in `Dmz` because it is the only Internet-facing application entry point.
- Put the business services in `AppTier` because they serve client requests and coordinate domain workflows.
- Put RabbitMQ and the async worker in `ProcTier` because they support internal asynchronous processing.
- Put MongoDB and MinIO in `DataTier` because they are persistent stores and must stay private.
- Put monitoring in `InfraZone` if you want observability to remain visible without polluting the core business tiers.

## Essential network and firewall rules

- Internet -> `Dmz`: allow only required public protocols such as HTTPS.
- `Dmz` -> `AppTier`: allow only the gateway-to-service application ports.
- `AppTier` -> `ProcTier`: allow only producer/consumer messaging flows needed to publish jobs or trigger workers.
- `ProcTier` -> `DataTier`: allow only the worker and approved services to reach MongoDB and MinIO.
- `AppTier` -> `DataTier`: allow only direct data access that is truly required by synchronous services.
- `InfraZone` -> all tiers: allow tightly controlled monitoring, logging, and health-check traffic.
- `SecZone` -> all tiers: allow only security-control traffic such as audit collection, secret retrieval, or policy enforcement.
- Never allow Internet -> `DataTier`.
- Avoid broad east-west access between tiers; prefer explicit allowlists per service flow.
- Restrict management access to private admin paths only, not through public application routes.

## Practical modeling advice

If a service both serves requests and runs heavy background jobs, keep the request-handling part in `AppTier` and move the worker runtime into `ProcTier`. That keeps the diagram readable and the security boundary clear.