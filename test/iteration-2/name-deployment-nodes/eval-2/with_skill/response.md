Use `ProdEuApiVm`, not `EuProdApiVm`.

Reason: it is the cleanest extension of the base pattern `{Environment}{Service}Vm`, expanded consistently to `{Environment}{Region}{Service}Vm`.

Recommended convention:

- EU VMs: `ProdEuApiVm`, `ProdEuWorkerVm`, `ProdEuDatabaseVm`
- US VMs: `ProdUsApiVm`, `ProdUsWorkerVm`, `ProdUsDatabaseVm`

Apply the same left-to-right order to zones and tiers:

- `ProdEuAppTier`, `ProdEuProcTier`, `ProdEuDataTier`
- `ProdUsAppTier`, `ProdUsProcTier`, `ProdUsDataTier`
- if you need a functional zone, use `ProdEuSecZone` and `ProdUsSecZone`

Keep these rules everywhere:

- PascalCase only
- environment first, region second, role third
- preserve the expected suffixes: `Vm`, `Tier`, `Zone`
- never mix patterns such as `ProdEuApiVm` in one area and `EuProdWorkerVm` in another

So pick one readable convention—`{Environment}{Region}{Role}`—and use it uniformly across the whole estate.
