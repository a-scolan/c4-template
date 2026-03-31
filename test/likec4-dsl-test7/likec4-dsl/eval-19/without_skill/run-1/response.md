- In `view backend of cloud.backend { include * }`, the base include set is the scoped set under `cloud.backend`: it includes its **direct children** (and, by scope expansion, their nested descendants), not the entire model.
- From that scoped include, you still see all relationships among the included elements, and additional neighboring elements/edges can be brought in when you add incoming/outgoing includes around `cloud.backend` (plus any implied/derived relations that result from those included endpoints).

```likec4
view backend of cloud.backend {
  include *
  include * -> cloud.backend
  include cloud.backend -> *
}
```