Use a “decision-first” description style for `ProdApiVm`: include only data operators need to triage, restore, or escalate.

Keep one compact table:

- **Network:** `eth0`, `eth1` (monitoring)
- **Platform:** OS, runtime
- **Capacity:** CPU, RAM, GPU, Disk
- **Reliability:** health check, restart policy, RTO/RPO

To prevent bloat:

- One line per property, no narrative paragraphs inside table rows.
- Exclude historical context and implementation trivia.
- Keep values current and measurable.
- Remove any field that no alert/runbook/action uses.

If automation needs it, mirror key properties in metadata (for example `eth0`, `os`, `cpu`, `ram`, `gpu`, `rto`). Otherwise keep metadata out and preserve readability.