For `ProdApiVm`, make the description a single **Markdown table** that operators can scan quickly.

Recommended order:
1. **Network interfaces first** — `eth0`, then `eth1` (mark `eth1` as monitoring if that is its purpose)
2. **Operating system**
3. **Hardware** — CPU, RAM, Disk, and GPU only if it matters operationally
4. **Service/runtime** — app role, container/runtime, health check
5. **Operational recovery data** — RTO/RPO and other high-signal facts

A good shape is:

| Property | Value |
|:---------|:------|
| eth0 | 10.x.x.x/24 |
| eth1 | 10.y.y.y/24 (monitoring) |
| OS | Ubuntu 22.04 |
| CPU | 4 vCPU |
| RAM | 16 GB |
| Disk | 200 GB SSD |
| Runtime | Docker 27 |
| Health Check | GET /health:8080 |
| RTO | 5 min |

Do **not** duplicate:
- the hostname/title already carried by the VM element
- **gateway** information for a normal VM — that belongs on the **zone/subnet**
- firewall rules, monitoring links, or service endpoints already shown by relationships/views
- tags inside metadata

`metadata {}` is optional. Add it only if automation, inventory, or compliance tooling will query fields such as `eth0`, `os`, `cpu`, or `rto`.
