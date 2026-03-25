```likec4
view detail extends backend-overview {
  include api
  include * -> cloud.backend
}
```

`detail` extends `backend-overview`, so it inherits the same base context/scope (`cloud.backend`). Because of that scope inheritance, `include api` is resolved relative to `cloud.backend` (effectively `cloud.backend.api`), so you don’t need to write the full FQN.

The relationship predicate `include * -> cloud.backend` adds all relationships whose target is `cloud.backend`, i.e., all incoming links from the rest of the model into `cloud.backend`.