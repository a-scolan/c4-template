`*` in a scoped view like:

`view backend of cloud.backend { include * }`

means **all elements inside the scope of `cloud.backend`** (the scoped element and its descendants, according to the scoped-view rules), not the entire model.

So no — it does **not** include the whole model by default.

Minimal snippet that keeps scoped elements and adds only 1-hop incoming/outgoing around `cloud.backend`:

```likec4
view backend of cloud.backend {
  include *
  include * -> cloud.backend
  include cloud.backend -> *
}
```