Keep `ProdApiVm` rich, but optimized for the first minute of operator triage — not as a full encyclopedia.

Use **one Markdown table** and keep the order:
1. `eth0`
2. `eth1` (monitoring)
3. OS
4. CPU / RAM / GPU / Disk
5. runtime or app role
6. health check / RTO / other top-priority operational facts

A practical pattern is:

| Property | Value |
|:---------|:------|
| eth0 | 10.1.0.12/24 |
| eth1 | 10.4.0.12/24 (monitoring) |
| OS | Ubuntu 22.04 LTS |
| CPU | 8 vCPU |
| RAM | 32 GB |
| GPU | NVIDIA T4 |
| Disk | 250 GB SSD |
| Runtime | Docker + API service |
| Health Check | GET /health:8080 every 30s |
| RTO | 10 min |

Keep **in** the VM block:
- network interfaces
- the core host/runtime specs an operator needs immediately
- only the operational facts that change triage or recovery

Move **out** to linked ops docs or runbooks if it becomes too detailed:
- full package lists
- driver or kernel tuning details
- long monitoring or alert matrices
- step-by-step recovery procedures
- capacity history and benchmark data

Also avoid duplicating data that belongs elsewhere:
- **gateway / subnet routing** -> zone description
- firewall / monitoring topology -> relationships or views
- hostname and tags -> already modeled on the element

If automation queries fields such as `eth0`, `gpu`, or `rto`, mirror those into `metadata {}`. Otherwise, skip metadata and keep the table human-first.

A good rule of thumb: if an operator would not need it in the first 30 seconds, link it instead of stuffing it into the VM block.
