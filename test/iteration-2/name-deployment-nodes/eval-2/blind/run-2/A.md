Choose **`ProdEuApiVm`**.

Keep naming order fixed everywhere: `{Environment}{Region}{Service}Vm`.

Examples:
- EU: `ProdEuApiVm`, `ProdEuWorkerVm`, `ProdEuDatabaseVm`
- US: `ProdUsApiVm`, `ProdUsWorkerVm`, `ProdUsDatabaseVm`

For zones, mirror the same ordering idea:
- `EuAppTier`, `EuProcTier`, `EuDataTier`
- `UsAppTier`, `UsProcTier`, `UsDataTier`

This gives predictable lexical grouping by environment first, then region, then role.