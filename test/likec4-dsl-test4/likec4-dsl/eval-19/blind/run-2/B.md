# Scoped View Semantics for `include *`

- **Base include set:** In a scoped element view (`view backend of cloud.backend { ... }`), `include *` resolves to the **direct children** of `cloud.backend` — i.e., all elements whose fully-qualified name is one level below `cloud.backend` (e.g. `cloud.backend.api`, `cloud.backend.db`). It does **not** recursively descend into grandchildren, nor does it include the whole model.

- **Neighboring / derived elements and relationships:** Because LikeC4 renders relationships between all visible nodes, any element that shares a direct relationship with one of those direct children (incoming or outgoing) can be pulled in as a neighbor — and its relationship edges will appear in the diagram. Additionally, the scoped element (`cloud.backend`) itself is always shown as the implicit boundary/container, and relationships crossing the boundary (to/from elements outside the scope) are surfaced as implicit edges.

## Minimal snippet — keeping `include *` and adding cross-boundary relationships

```likec4
view backend of cloud.backend {
  include *             // direct children of cloud.backend
  include cloud.backend // ensure the parent boundary is visible
  include -> cloud.backend ->  // incoming and outgoing relationships of cloud.backend itself
}
```

> `-> cloud.backend ->` is the shorthand for "any element that has a relationship **to** `cloud.backend`, plus any element that `cloud.backend` has a relationship **to**", making all neighboring nodes and their edges visible alongside the local subtree.
