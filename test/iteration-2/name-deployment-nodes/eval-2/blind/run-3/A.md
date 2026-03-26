Prefer **`ProdEuApiVm`**.

Use one canonical order for all VM names:

`{Environment}{Region}{Service}Vm`

So:
- `ProdEuApiVm`, `ProdEuWorkerVm`, `ProdEuDatabaseVm`
- `ProdUsApiVm`, `ProdUsWorkerVm`, `ProdUsDatabaseVm`

For zones, apply the same readability pattern with regional prefix:
- `EuAppTier`, `EuProcTier`, `EuDataTier`
- `UsAppTier`, `UsProcTier`, `UsDataTier`

Why this works: environment-first grouping keeps production assets together, then splits by region, then service role.