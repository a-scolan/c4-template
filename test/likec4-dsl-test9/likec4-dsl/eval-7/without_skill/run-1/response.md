## Detail view

```likec4
view detail extends backend-overview {
  include api
  include * -> cloud.backend
}
```

`detail` extends `backend-overview`, so it inherits the same base scope: `cloud.backend`.
That is why `include api` resolves to `cloud.backend.api` automatically, without needing the full FQN.

Here, **scope inheritance** means the child view keeps the `of cloud.backend` context from the parent view. In practice, any relative element reference inside the derived view is resolved from that same scope unless you explicitly write a full FQN.

The relationship predicate `include * -> cloud.backend` adds every incoming relationship whose target is `cloud.backend`, pulling in the external source elements needed to show those incoming connections.