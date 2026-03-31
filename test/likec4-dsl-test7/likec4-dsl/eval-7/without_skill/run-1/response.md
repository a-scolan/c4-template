```likec4
view backend-detail extends backend-overview {
  include api
  include * -> cloud.backend
}
```

`backend-detail` extends `backend-overview`, so it inherits the same base scope (`of cloud.backend`) and everything already included there.

That is why `include api` works without the full FQN `cloud.backend.api`: inside this inherited scope, `api` is resolved relative to `cloud.backend`.

The relationship predicate `include * -> cloud.backend` adds all incoming relationships targeting `cloud.backend` from anywhere else in the model.