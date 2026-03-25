In a scoped view like:

```likec4
view backend of cloud.backend {
  include *
}
```

`*` **does not include the whole model**.
In scoped-view semantics, `*` includes:
- the scoped element itself (`cloud.backend`),
- its **direct children**,
- and relationships involving that included set.

A minimal snippet that keeps that scope and then adds only incoming/outgoing relationships around `cloud.backend` is:

```likec4
views {
  view backend of cloud.backend {
    include *
    include * -> cloud.backend
    include cloud.backend -> *
  }
}
```