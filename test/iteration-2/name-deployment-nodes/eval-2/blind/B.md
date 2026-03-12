Choose `ProdEuApiVm`, not `EuProdApiVm`.

The base convention is environment first, so extend it consistently as:

- VMs: `{Environment}{Region}{Service}Vm`
- Tier zones: `{Environment}{Region}{Tier}Tier`
- Functional zones: `{Environment}{Region}{Function}Zone`

Examples:

- `ProdEuApiVm`, `ProdEuWorkerVm`, `ProdEuDbVm`
- `ProdUsApiVm`, `ProdUsWorkerVm`, `ProdUsDbVm`
- `ProdEuAppTier`, `ProdEuProcTier`, `ProdEuDataTier`
- `ProdUsAppTier`, `ProdUsProcTier`, `ProdUsDataTier`
- If needed: `ProdEuSecZone`, `ProdUsInfraZone`

The important part is not EU vs US first by itself; it is using one order everywhere. If you start with environment-first, keep it environment-first for every VM and every zone.

So avoid mixed estates like these:

- `ProdEuApiVm` next to `UsProdWorkerVm`
- `ProdEuAppTier` next to `EuProdDataTier`

Pick one readable order, keep PascalCase, and preserve the expected suffixes: `Vm`, `Tier`, and `Zone`.