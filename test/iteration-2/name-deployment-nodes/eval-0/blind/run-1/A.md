Use this naming set:

- **Environment:** `Prod`
- **Zones (tier-style):** `Dmz`, `AppTier`, `ProcTier`, `DataTier`, `SecZone`
- **VMs:**
  - `ProdApigwVm`
  - `ProdUploadVm`
  - `ProdWorkerVm`
  - `ProdDatabaseVm` (MongoDB)
  - `ProdMonitoringVm`

Fixed candidates:

- `ProdApiVM` → **`ProdApigwVm`** (use `Vm`, not `VM`; keep service token consistent)
- `prod_upload_vm` → **`ProdUploadVm`** (PascalCase identifier for node name)
- `AppServers` → **`AppTier`** (zone should use tier/zone convention)
- `MonitoringTier` → **`SecZone`** (if monitoring/security function zone) or **`ProcTier`** (if worker processing layer)

If you prefer strict layered tiers only, keep `MonitoringTier` as **`ProcTier`** and place monitoring stack there. If you want function-based segregation, use **`SecZone`**.