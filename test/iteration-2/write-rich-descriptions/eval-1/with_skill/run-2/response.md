For `ProdApiVm`, make the description operationally scannable with one table and strict ordering:

1. **Network first**: `eth0`, then `eth1` (monitoring)
2. **OS**
3. **Hardware**: CPU, RAM, Disk, GPU if relevant
4. **Runtime/service**: runtime, process/container detail, health endpoint
5. **Operations**: RTO/RPO, backup or failover notes (only essentials)

Avoid duplication:

- Hostname (already encoded in VM/node title)
- Gateway in VM details (normally belongs to zone)
- Firewall and topology rules (represented by relationships)
- Monitoring/link endpoints already expressed via model connections
- Tags copied into metadata

Metadata is optional: only include keys that downstream automation will actually query.