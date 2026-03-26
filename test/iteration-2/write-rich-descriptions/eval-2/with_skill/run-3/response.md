To keep `ProdApiVm` rich but not bloated, optimize for incident handling, not encyclopedic completeness.

Recommended pattern:

- One compact table only.
- Ordered fields: network (`eth0`, `eth1`) → platform → capacity (CPU/RAM/GPU/Disk) → operational reliability.
- Prefer short measurable values over explanatory prose.

A good inclusion test: *Would this row change an on-call decision in the next 5 minutes?*
- If yes, keep it.
- If no, move it to ADR/runbook/docs.

Add metadata duplicates only when queried by automation pipelines. Otherwise, keep metadata absent and preserve human scan speed.