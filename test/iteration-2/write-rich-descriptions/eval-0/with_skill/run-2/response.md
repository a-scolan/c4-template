Use `create-element` first, then `write-rich-descriptions`.

Reason: rich descriptions should be attached to existing model elements. If the processing service and production VM are still hypothetical, create them first.

Then pick format by type:

- **Processing service (system model)**
  - Keep concise prose + `technology`.
  - Add `metadata {}` only for queryable fields you actually use (for example `owner`, `regions`).
  - Do not place SLA/RTO/RPO at container/service level.

- **Production VM (deployment model)**
  - Use a markdown table in `description`.
  - Order: network interfaces first (`eth0`, `eth1`), then OS, hardware, runtime/service, operational details.
  - Add metadata duplicates only if automation needs machine-queryable values.

So the sequence is: create elements → apply rich descriptions with sparse, intentional metadata.