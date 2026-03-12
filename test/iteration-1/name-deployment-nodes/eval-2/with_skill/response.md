Use `ProdEuApiVm`, not `EuProdApiVm`.

A clean extension of the base convention is:

- VMs: `{Environment}{Region}{Service}Vm`
- Tier zones: `{Environment}{Region}{Tier}Tier`
- Functional zones: `{Environment}{Region}{Function}Zone`

Example set:

- Environments: `ProdEu`, `ProdUs`
- Zones: `ProdEuAppTier`, `ProdEuProcTier`, `ProdEuDataTier`, `ProdUsAppTier`, `ProdUsProcTier`, `ProdUsDataTier`
- VMs: `ProdEuApiVm`, `ProdEuWorkerVm`, `ProdEuDatabaseVm`, `ProdUsApiVm`, `ProdUsWorkerVm`, `ProdUsDatabaseVm`

The key is not whether region comes first in isolation; it is that you extend the original `{Environment}{Service}Vm` pattern in one consistent direction. If you choose environment first, keep it everywhere.

So do not mix variants like `ProdEuApiVm` in one place and `EuProdDatabaseVm` in another. Stick to one scan-friendly PascalCase order with the expected suffixes: `Vm`, `Tier`, and `Zone`.