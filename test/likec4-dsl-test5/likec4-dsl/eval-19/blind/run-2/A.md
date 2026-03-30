- In a scoped view `of cloud.backend`, `include *` starts from the scope and includes its in-scope structure, i.e. `cloud.backend` and its **direct children** (and nested descendants).
- External neighbors are not part of that base set, but they can become visible when you include incoming/outgoing relations around `cloud.backend`; those added edges can also bring the connected outside elements into the rendered view.

```likec4
view backend of cloud.backend {
  include *
  include -> cloud.backend
  include cloud.backend ->
}
```# Scoped view `include *` semantics

- **Base include set:** In a scoped view (`view backend of cloud.backend { ... }`), `*` resolves to the **direct children** of the subject element — i.e., every element whose fully-qualified name is one level below `cloud.backend` (e.g. `cloud.backend.api`, `cloud.backend.db`). It does **not** automatically pull in the whole model, nor does it recurse into grandchildren.

- **Neighboring / derived visibility:** Because LikeC4 auto-resolves relationships between any two already-included nodes, edges that connect those direct children to each other are rendered automatically. Additionally, if you explicitly add relationship-based predicates (see snippet below), the external endpoints of those edges — elements outside the subtree — become visible as neighboring nodes in the diagram.

## Minimal snippet

```likec4
view backend of cloud.backend {
  include *               // direct children of cloud.backend

  // pull in whatever points INTO cloud.backend from outside
  include -> cloud.backend

  // pull in whatever cloud.backend points OUT TO
  include cloud.backend ->
}
```

The two extra `include` lines bring in the immediate upstream callers and downstream dependencies of `cloud.backend` itself (as collapsed neighbor boxes), while `include *` keeps all direct children expanded inside the boundary.
