- Base include set: in `view backend of cloud.backend`, `include *` starts from `cloud.backend` and its direct children, then includes the scoped subtree beneath `cloud.backend`; it does **not** mean the entire model or unrelated siblings outside that scope.
- Extra visibility: relationships among those included elements are shown, and implied/promoted relationships plus explicit edge includes can still surface neighboring external elements that connect to `cloud.backend`.

```likec4
view backend of cloud.backend {
  include *
  include * -> cloud.backend
  include cloud.backend -> *
}
```