No — that relationship is **invalid**.

`cloud` is the parent of `backend`, and LikeC4 does not allow relationships between parent/child elements.

A minimal valid pattern is to keep the hierarchy, then add relationships between non-parent-child elements (for example, from an external actor to `backend`):

```likec4
model {
  customer = actor 'Customer'

  cloud = system 'Cloud' {
    backend = container 'Backend'
  }

  customer -> cloud.backend 'uses'
}
```

This preserves the `cloud -> backend` containment structurally (via nesting) and adds a valid behavioral relationship elsewhere.