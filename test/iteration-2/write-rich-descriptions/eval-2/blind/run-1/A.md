Great data set—now compress it for operators.

Use a **single table**, but only keep fields that change decisions during incidents.

Practical structure:

- **Network (first):** `eth0`, `eth1 (monitoring)`
- **Platform:** OS, runtime
- **Capacity:** CPU, RAM, GPU, Disk
- **Ops-critical:** health check, restart policy, RTO/RPO

How to avoid “encyclopedia mode”:

- Keep one value per property (no long narratives inside cells).
- Move history/rationale to ADR/docs, not VM description.
- Keep only currently actionable operational facts.
- If a value is not queried/used, remove it.

Suggested compact example table layout:

- `eth0`: primary subnet CIDR
- `eth1`: monitoring subnet CIDR
- `OS`: exact distro/version
- `CPU` / `RAM` / `GPU` / `Disk`
- `Runtime`: e.g., Docker + version
- `Health Check`: endpoint + interval
- `RTO` (and `RPO` if applicable)

Optional metadata duplication is fine only when automation needs machine-queryable fields (e.g., `eth0`, `os`, `cpu`, `ram`, `gpu`, `rto`).