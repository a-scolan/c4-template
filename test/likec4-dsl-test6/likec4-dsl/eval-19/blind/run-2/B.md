- `include *` in a scoped view starts from the scoped element and includes its direct children as the base set, not the entire model.
- From that scoped base, neighboring elements and the relevant edges can still become visible when you include relationships around `cloud.backend`; those relationship includes can pull in external sources/targets connected to the scoped element.

```likec4
view backend of cloud.backend {
  include *
  include * -> cloud.backend
  include cloud.backend -> *
}
```