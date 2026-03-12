Use `ProdEuApiVm`, not `EuProdApiVm`.

A readable convention is to extend the base pattern in one direction only:

- VMs: `{Environment}{Region}{Service}Vm`
- Tier zones: `{Environment}{Region}{Role}Tier`
- Functional zones: `{Environment}{Region}{Function}Zone`

Examples:

- EU VMs: `ProdEuApiVm`, `ProdEuWorkerVm`, `ProdEuDbVm`
- US VMs: `ProdUsApiVm`, `ProdUsWorkerVm`, `ProdUsDbVm`
- EU zones: `ProdEuAppTier`, `ProdEuProcTier`, `ProdEuDataTier`
- US zones: `ProdUsAppTier`, `ProdUsProcTier`, `ProdUsDataTier`
- Functional zones if needed: `ProdEuSecZone`, `ProdUsInfraZone`

Do not mix `ProdEu...` and `EuProd...` in the same estate. Pick one order, keep PascalCase everywhere, and preserve the expected suffixes: `Vm`, `Tier`, and `Zone`.