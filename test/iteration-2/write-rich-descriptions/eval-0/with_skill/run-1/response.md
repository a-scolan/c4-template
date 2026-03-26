Use `create-element` first, then apply `write-rich-descriptions`.

Why first: descriptions should be attached to real elements; if the processing service and `ProdApiVm` do not exist yet, create them before enriching description blocks.

After creation, choose format by element type:

- **Processing service (system model element)**
  - Use concise prose description + `technology`.
  - Add `metadata {}` only for fields you will actually query (for example `owner` or `regions`).
  - Keep SLA/RTO/RPO at **system** level, not container/service level.

- **Production VM (deployment element)**
  - Use a markdown table in `description` for operator readability.
  - Put network interfaces first (`eth0`, then `eth1`), then OS, hardware, service/runtime, operational items.
  - Optional: duplicate key table values into `metadata {}` only if automation queries them.

In short: create element first, then write rich description; metadata is sparse and purpose-driven.