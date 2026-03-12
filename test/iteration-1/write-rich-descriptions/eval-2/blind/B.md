Write `ProdApiVm` as a concise **ops-useful Markdown table**, not as a long prose dump.

Keep the description focused on what an operator needs first:

| Property | Value |
|:---------|:------|
| eth0 | primary application network |
| eth1 | monitoring network |
| OS | ... |
| CPU | ... |
| RAM | ... |
| GPU | include only if the workload depends on it operationally |
| Disk | ... |
| Container Runtime / Service | ... |
| Health Check | ... |
| RTO / RPO | ... |

Use this priority order:

1. `eth0`
2. `eth1` monitoring
3. OS
4. CPU / RAM / GPU / Disk
5. runtime or service details
6. critical operational fields such as health checks and RTO/RPO

To avoid turning the block into an encyclopedia:

- Keep only the fields that help someone operate, troubleshoot, or recover the VM.
- Include GPU details only if they affect scheduling, capacity, or runtime behavior.
- Move overly fine-grained details—full package inventories, long tuning notes, exhaustive compliance data, or detailed runbooks—into separate operations documentation and link to it if needed.
- Keep metadata optional; use it only when automation queries those values.

Also avoid duplication:

- Do not repeat gateway details that belong to the zone.
- Do not restate firewall or monitoring relationships already shown in the model.
- Do not duplicate identifiers already present in the VM title.

That gives you a rich description that stays readable: network first, core platform facts next, critical operations data last, and deep detail externalized.