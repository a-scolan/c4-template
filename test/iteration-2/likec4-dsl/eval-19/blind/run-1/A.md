In scoped view semantics, `*` is relative to the view scope. So in `view backend of cloud.backend { include * }`, the `*` does **not** mean the whole model. It means: include everything that belongs to the scope of `cloud.backend` for that view — effectively the scoped element and its nested content, not unrelated elements elsewhere in the model.

A minimal pattern to keep the scoped content and also bring in only first-hop incoming and outgoing relationships around `cloud.backend` is:

view backend of cloud.backend {
  include *
  include * -> cloud.backend
  include cloud.backend -> *
}

That keeps the view scoped to `cloud.backend`, then adds only direct neighbors that connect into or out of `cloud.backend`, rather than expanding to the entire model.
