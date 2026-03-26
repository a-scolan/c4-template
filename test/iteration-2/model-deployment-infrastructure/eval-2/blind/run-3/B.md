Great case for an “honest abstraction.”

If Kubernetes is managed and host internals are not visible, keep the required hierarchy without inventing fake machines:

- `Prod` (Environment)
  - `AppTier` (Zone)
    - one VM-level placeholder such as `ProdK8sWorkersVm` (explicitly described as provider-managed node pool, not a specific host)
      - `apiApp`, `uploadApp`, `workerApp` as `Node_App`

Then wire each `Node_App` with `instanceOf` to logical containers:

- `apiApp { instanceOf platform.apiGateway }`
- `uploadApp { instanceOf platform.uploadService }`
- `workerApp { instanceOf platform.processingWorker }`

And for data if managed DB exists:

- `mongoApp { instanceOf platform.mongoDb }` in `DataTier` (or managed DB zone)

Key point: document uncertainty transparently in descriptions (managed service, no host-level access) instead of fabricating per-node VM details.