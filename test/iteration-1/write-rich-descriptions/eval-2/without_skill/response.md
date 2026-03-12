Write it as a Markdown table that keeps only the facts an operator needs to understand, diagnose, or change the VM safely.

Keep this order:

1. `eth0`
2. `eth1`
3. Hosted role
4. Platform / runtime
5. Capacity
6. Key operations
7. Ownership / references

A good shape is:

| Topic | Content |
| --- | --- |
| `eth0` | primary traffic path, zone or network, IP or DHCP, external or internal exposure |
| `eth1` | monitoring, admin, or back-end path, zone or network, IP or DHCP |
| Role | API workload, major responsibility, critical dependencies |
| Platform | OS or image baseline, virtualization or runtime notes |
| Capacity | vCPU, RAM, GPU, storage summary relevant to triage and capacity |
| Operations | monitoring, backup, patch window, reboot or failover expectations |
| Ownership | owning team, on-call, runbook or reference links |

Keep in the description:

- interface purpose and placement
- role of the VM
- capacity numbers that matter for operations
- only the most important monitoring and recovery facts

Externalize when it gets too fine-grained:

- exhaustive package lists
- every GPU tuning flag
- full disk partition maps
- long threshold catalogs
- full runbook procedures
- anything better maintained in CMDB, infrastructure-as-code, or operations docs

Avoid duplication:

- do not repeat gateway, subnet policy, or zone-wide rules that belong to the zone or subnet
- do not restate information already captured in separate operations documentation
- keep metadata optional, only for fields that automation must read

The test is simple: if a person on call needs it in the first minute, keep it; if they only need it during deep investigation, link out to it.
