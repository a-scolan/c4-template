# Scoped view semantics for `include *`

- **Base include set:** In a scoped element view (`view backend of cloud.backend { ... }`), `include *` resolves to the **direct children** of the scoped element (`cloud.backend`), i.e. all elements whose parent FQN is exactly `cloud.backend`.

- **Neighboring/derived visibility:** Because LikeC4 renders relationships between any two nodes that are both present in the view, elements that have direct relationships *to* or *from* `cloud.backend` (or its direct children) will have those edges drawn if the related endpoint is also in scope; additionally, using `include cloud.backend.*` alongside relationship wildcards can pull in immediate neighbors — but with bare `include *` inside the scoped view, only the children and their intra-subtree relationships are included by default. Relationship lines to elements *outside* the subtree are not shown unless those external elements are also explicitly included (e.g. with `include cloud.backend ->, -> cloud.backend`).

## Minimal snippet

```likec4
view backend of cloud.backend {
  include *

  // incoming relationships to cloud.backend (and its children)
  include -> cloud.backend
  // outgoing relationships from cloud.backend (and its children)
  include cloud.backend ->
}
```
