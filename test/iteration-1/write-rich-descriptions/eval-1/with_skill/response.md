For `ProdApiVm`, use a **Markdown table** in the description so operators can scan the VM quickly.

Recommended order:

1. **Network interfaces first**: `eth0`, then `eth1` if present
2. **Operating system**
3. **Hardware**: CPU, RAM, Disk, GPU only if it matters operationally
4. **Application or runtime details**: container runtime, service role, health check
5. **Operational data**: RTO, RPO, backup/restore note, monitoring port if relevant

A good shape is:

| Property | Value |
|:---------|:------|
| eth0 | primary application network |
| eth1 | monitoring network |
| OS | ... |
| CPU | ... |
| RAM | ... |
| Disk | ... |
| GPU | ... |
| Health Check | ... |
| RTO | ... |

Do **not** duplicate information that already belongs elsewhere:

- Do not repeat the hostname if it is already the VM title.
- Do not put standard **gateway** information in the VM block; that normally belongs to the **zone** description.
- Do not restate firewall flows, monitoring relationships, or service endpoints that are already modeled through relationships.
- Do not duplicate tags in the description.

Add a `metadata { }` block only if automation needs to query values such as IPs, OS, CPU, RAM, Disk, or RTO. Otherwise, keep the VM description table human-focused and lean.