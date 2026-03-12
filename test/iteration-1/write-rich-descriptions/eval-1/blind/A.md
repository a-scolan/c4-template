For a future `ProdApiVm`, use a short Markdown table ordered by operational usefulness, not by exhaustiveness.

Recommended order:

1. **Network interfaces first**
   - `eth0`: primary purpose, network or zone, addressing mode, exposure
   - `eth1`: secondary, monitoring, admin, or back-end purpose, network or zone, addressing mode
2. **Hosted role**
   - what runs here and why this VM exists
3. **OS / runtime baseline**
   - OS, virtualization class, and key runtime only if it matters operationally
4. **Capacity**
   - vCPU, RAM, GPU, and storage summary at the level operators use for triage and capacity
5. **Operational controls**
   - monitoring, backup, patching or reboot expectations, recovery notes
6. **Ownership / support**
   - owner, on-call group, runbook link
7. **Optional machine-readable metadata**
   - keep this optional, and add it only when automation, filtering, or generation needs it

What not to duplicate:

- Do not repeat gateway details in the VM block unless this VM is a special routing case. Gateway information usually belongs to the network zone or subnet.
- Do not restate zone-level firewall, VLAN, or routing conventions that are already documented at the zone level.
- Do not copy full CMDB or runbook content into the VM description.

A compact table like this works well:

| Topic | What to capture |
| --- | --- |
| `eth0` | primary interface, zone or network, IP or DHCP, exposure |
| `eth1` | secondary or monitoring interface, zone or network, IP or DHCP |
| Role | API workload hosted on the VM |
| Platform | OS, hypervisor, or image baseline |
| Capacity | vCPU, RAM, GPU, storage summary |
| Operations | monitoring, backup, patching, restart or recovery notes |
| Ownership | team, support contact, runbook |

This keeps the VM description useful for operations without turning it into an encyclopedia.
