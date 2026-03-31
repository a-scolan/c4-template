```likec4
view detail extends backend-overview {
  include api
  include * -> cloud.backend
}
```

`detail` extends `backend-overview`, so it inherits that base view's scope: `cloud.backend`.
Because of that inherited scope, `include api` is resolved relative to `cloud.backend`, so it means `cloud.backend.api` without repeating the full FQN.

The relationship predicate `* -> cloud.backend` adds every incoming relationship whose target is `cloud.backend`, from anywhere else in the model.