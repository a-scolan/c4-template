Start with `create-element`, then use `write-rich-descriptions`.

Because the service and VM do not exist yet, create them first; otherwise you are documenting placeholders.

After creation:

- **Processing service (system model):** concise prose + technology; metadata only when query-driven (`owner`, `regions`, etc.).
- **Production VM (deployment model):** markdown table focused on operations, with interfaces first (`eth0`, `eth1`), then OS, hardware, runtime, operational recovery fields.

Keep metadata optional and sparse. Add it only if tooling/automation will query those keys.