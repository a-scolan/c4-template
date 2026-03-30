B — In a scoped element view, `include *` resolves to the scoped element itself (`cloud.backend`) plus its **direct children** as the base include set (one level only, not the full recursive subtree and not the whole model).

```likec4
view backend of cloud.backend {
  include *
  include -> cloud.backend
}
```

The second `include` line adds all elements that have an outgoing relationship into `cloud.backend` (i.e. its incoming relationships), while `include *` keeps the element and its direct children.
