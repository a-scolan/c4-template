Valid as written.

`backend-detail` inherits the base view’s scope from `backend-overview`, so you do not need to repeat `of cloud.backend`. With `extends`, the child view keeps the parent context and rules, then adds its own rules (here, `include api` and incoming relationships to `cloud.backend`).

```likec4
view backend-overview of cloud.backend {
  include *
}

view backend-detail extends backend-overview {
  include api
  include -> cloud.backend
}
```Error: Unable to read eval prompt in this benchmark mode due read-scope restrictions (with_skill_targeted), so no prompt-specific answer could be generated.