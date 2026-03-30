- In a scoped view, `include *` starts from the scoped element itself plus its **direct children**, not the entire model and not all recursive descendants.
- Because that scoped wildcard also includes relationships involving those included nodes, neighboring elements outside the local subtree can still appear as relationship endpoints, and those connected relationships can become visible too.

```likec4
view backend of cloud.backend {
  include *
  include -> cloud.backend ->
}
```