```likec4
view backend-detail of cloud.backend {
  extends backend-overview

  include api
  include * -> cloud.backend
}
```

`scope` inheritance here means the child view keeps the same base element context as the parent (`of cloud.backend`). Because of that, `api` is resolved relative to `cloud.backend`, so `include api` is equivalent to `include cloud.backend.api` without repeating the full FQN.

The relationship predicate `include * -> cloud.backend` pulls in all incoming relationships targeting `cloud.backend` from anywhere else in the model.