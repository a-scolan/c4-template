- In a scoped view (`view ... of cloud.backend`), `include *` starts from the scope and includes its **direct children** (the base include set), not the entire global model.
- From that scoped base, additional neighboring context can still appear when explicitly included (for example incoming/outgoing around the scoped element), along with the corresponding visible relationships.

```likec4
view backend of cloud.backend {
  include *
  include * -> cloud.backend
  include cloud.backend -> *
}
```
# Scoped View `include *` Semantics

- **Base include set:** In `view backend of cloud.backend { include * }`, the `*` resolves to the **direct children** of the scoped element `cloud.backend` (i.e., every element whose FQN is one level below `cloud.backend`, such as `cloud.backend.api`, `cloud.backend.db`, etc.), plus `cloud.backend` itself as the scope root. Relationships between those included elements are rendered automatically.

- **Neighboring / derived visibility:** Because the included children carry their relationships, any element outside the scope that is connected to a direct child via an explicit relationship edge can become visible when you add relationship-wildcard predicates (e.g., `include -> cloud.backend ->` or `include -> cloud.backend.*`). Without such predicates the outside neighbors are **not** pulled in automatically; the scoped include stays local. However, if an included child element itself has nested descendants with outgoing/incoming relationships declared in the model, those relationship lines (and their remote endpoints) surface as soon as you expand those relationship selectors.

## Minimal snippet

```likec4
view backend of cloud.backend {
  include *

  // pull in every element that sends to cloud.backend (incomers)
  include -> cloud.backend

  // pull in every element that cloud.backend sends to (outgoers)
  include cloud.backend ->
}
```

This keeps `include *` for the local subtree and adds two relationship selectors to make callers and callees of `cloud.backend` visible alongside the direct children.
