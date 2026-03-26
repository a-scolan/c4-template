For a future `ProdApiVm`, keep it ops-useful with **one compact table** in this order:

1. **Network first**
   - `eth0` (primary)
   - `eth1` (monitoring/secondary)
2. **OS**
3. **Hardware**
   - CPU, RAM, Disk, GPU (only if relevant)
4. **Runtime / service details**
   - container/runtime or process model
   - health check endpoint + cadence
5. **Operational items**
   - RTO/RPO, backup policy, alerting-relevant facts

What not to duplicate:

- Hostname (already in node title)
- Gateway in VM table (belongs at zone level in normal cases)
- Firewall/flow rules (belong in relationships/diagram)
- Monitoring links and endpoint relationships (model relationships already express these)
- Tags in metadata (use `#tags`)

Use metadata only if queried by automation (inventory/compliance/capacity workflows). Otherwise table + concise prose is enough.