`*` in a scoped view means **all elements within that scope**, not the whole model.

So in:

`view backend of cloud.backend { include * }`

`*` includes `cloud.backend` and its in-scope descendants (depending on nesting), **not every element in `cloud` or the entire workspace model**.

A minimal example that keeps scoped contents and adds only direct incoming/outgoing neighbors of `cloud.backend`:

```likec4
model {
  cloud = system "Cloud" {
    backend = container "Backend"
    frontend = container "Frontend"
    db = container "Database"

    frontend -> backend "calls"
    backend -> db "reads/writes"
  }
}

views {
  view backend of cloud.backend {
    include *
    include * -> cloud.backend
    include cloud.backend -> *
  }
}
```