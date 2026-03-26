In `view backend of cloud.backend`, `include *` is scoped: it includes elements in that view scope, not the whole model.

```likec4
view backend of cloud.backend {
  include *
  include * -> cloud.backend
  include cloud.backend -> *
}
```