Use **`ProdEuApiVm`**, not `EuProdApiVm`.

A readable global convention is:
- **Environment first**
- **Region second**
- **Zone or tier third** when needed
- **Workload role fourth**
- **Kind suffix last** (`Zone`, `Vm`, `App`)

Recommended pattern:
- `<Env><Region><Role>Vm`
- `<Env><Region><Tier>Zone`
- `<Env><Region><Role>App`

Examples:
- `ProdEuApiVm`
- `ProdEuWorkerVm`
- `ProdEuDatabaseVm`
- `ProdEuAppZone`
- `ProdEuDataZone`
- `ProdUsApiVm`
- `ProdUsWorkerVm`
- `ProdUsDatabaseVm`

Why `ProdEuApiVm` is better:
- It groups all production nodes together when sorted alphabetically.
- It keeps the highest-level discriminator first.
- It scales well when you later add `DevEu...`, `TestEu...`, and `ProdUs...`.

To keep one readable convention across all names, pick exactly one order and never mix it:

1. **Environment**: `Prod`, `Dev`, `Test`
2. **Region**: `Eu`, `Us`
3. **Zone/Tier**: `Dmz`, `App`, `Data`, `Ops` when needed
4. **Role**: `Api`, `Worker`, `Database`
5. **Kind**: `Zone`, `Vm`, `App`

So a consistent multi-region set could be:
- `ProdEuDmzZone`
- `ProdEuApiVm`
- `ProdEuWorkerVm`
- `ProdEuDataZone`
- `ProdEuDatabaseVm`
- `ProdUsDmzZone`
- `ProdUsApiVm`
- `ProdUsWorkerVm`
- `ProdUsDataZone`
- `ProdUsDatabaseVm`

One small but important rule: do not alternate between `Db`, `Database`, `VM`, and `Vm`. Pick one vocabulary and keep it boringly consistent — boring names are excellent names.
Prefer **`prod-eu-api-vm-01` style**, i.e. equivalent to **`EuProdApiVm` ordering? No**. Put environment first.

So between your two options:

Recommended canonical order:
1. environment (`prod`)
2. geography (`eu` / `us`)
3. optional zone (`w1`, `e1`, `a`, `b`)
4. workload role (`api`, `worker`, `db`)
5. resource type (`vm`, `zone`, `env`)
6. ordinal (`01`, `02`)

Examples for multi-region prod:

Readability guardrails:
