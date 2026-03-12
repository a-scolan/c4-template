Use this convention:

- Environment: `Prod`
- Tier zones: `Dmz`, `AppTier`, `ProcTier`, `DataTier`
- Functional zone for monitoring/security tooling: `SecZone` (or `InfraZone` if it is mainly ops/platform infrastructure)
- VMs:
  - `ProdApigwVm`
  - `ProdUploadVm`
  - `ProdWorkerVm`
  - `ProdDatabaseVm`
  - `ProdMonitoringVm`

Fix the candidates:

- `ProdApiVM` → `ProdApigwVm`
- `prod_upload_vm` → `ProdUploadVm`
- `AppServers` → `AppTier`
- `MonitoringTier` → `SecZone`

Rules to keep:

- PascalCase identifiers
- VM names follow `{Environment}{Service}Vm`
- Use `Vm`, not `VM`
- Use tier names like `AppTier` and `DataTier` for layered zones
- Use functional names like `SecZone` and `InfraZone` for specialized zones
