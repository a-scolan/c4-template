Use this deployment hierarchy in `deployment.c4`:

- `Prod` (Environment)
  - `Dmz` / `AppTier` / `ProcTier` / `DataTier` (Zones)
    - `ProdApigwVm`, `ProdUploadVm`, `ProdWorkerVm`, `ProdMongoVm` (VM nodes)
      - `apiApp`, `uploadApp`, `workerApp`, `mongoApp` (`Node_App` instances)

Minimal LikeC4 skeleton:

- `Prod = Node_Environment "Production" { ... }`
- `Dmz = Zone "DMZ" { ... }`
- `ProdApigwVm = Node_Vm "prod-apigw-vm" { ... }`
- `apiApp = Node_App "API Gateway" { instanceOf platform.apiGateway }`

Apply the same for upload/worker/mongo with `instanceOf` pointing to the logical container FQNs (for example `platform.uploadService`, `platform.processingWorker`, `platform.mongoDb`).

Important rule: do **not** manually copy normal app traffic relationships in deployment. Relationships between deployed instances are inherited through `instanceOf` from the logical model. Add deployment relationships only for infrastructure-only links (monitoring, backup, bastion, replication, etc.).