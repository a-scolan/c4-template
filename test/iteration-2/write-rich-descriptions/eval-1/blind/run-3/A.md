For `ProdApiVm`, include information in this exact practical sequence:

1. `eth0`, then `eth1` (monitoring)
2. OS/version
3. CPU, RAM, Disk, GPU (if materially used)
4. Runtime + service health probe
5. RTO/RPO and other recovery-critical details

Keep it useful by excluding duplicates:

- Hostname (already in element/node name)
- Gateway at VM level (zone-level in normal topology)
- Firewall/topology details already modeled as relationships
- Monitoring links/endpoints already represented in diagram relationships
- Tags repeated inside metadata

Use metadata only for machine queries; otherwise, table + concise prose is the right balance.