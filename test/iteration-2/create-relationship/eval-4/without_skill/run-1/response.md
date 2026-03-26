Usually, **don’t keep** `Prod.Web.webApp -[https]-> Prod.App.apiApp` in deployment for normal app traffic.

In this workspace’s modeling rules:
- Normal application interactions belong in the **system model** and are inherited by deployment via `instanceOf`.
- Deployment relationships are for **infrastructure-specific** links.

Where protocol labels belong:
- `Manual` → system-model relationship technology for human interaction (e.g., user to web app)
- `HTTPS` → system-model relationship technology for secure API call
- `HTTP/8080` → system-model relationship technology when non-default port matters

So keep protocol/interaction technology on model relationships; use deployment edges only when you need infra-only connectivity details.
