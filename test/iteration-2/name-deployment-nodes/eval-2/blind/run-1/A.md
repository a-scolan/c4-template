Use **`ProdEuApiVm`**, not `EuProdApiVm`.

Reason: keep one fixed left-to-right order:

1. **Environment** (`Prod`)
2. **Region** (`Eu`, `Us`)
3. **Service** (`Api`, `Worker`, `Database`)
4. **Suffix** (`Vm`)

Recommended convention:

- **VMs:** `{Environment}{Region}{Service}Vm`
  - `ProdEuApiVm`, `ProdEuWorkerVm`, `ProdEuDatabaseVm`
  - `ProdUsApiVm`, `ProdUsWorkerVm`, `ProdUsDatabaseVm`

- **Zones:** `{Region}{Tier}Tier` (or `{Region}{Function}Zone`)
  - `EuAppTier`, `EuProcTier`, `EuDataTier`
  - `UsAppTier`, `UsProcTier`, `UsDataTier`

- **Environment node:**
  - Single environment: `Prod`
  - If you model each region as separate env nodes, use `ProdEu` and `ProdUs` consistently.

Keep this rule immutable across the repo and apply it to every new node to preserve scan readability.