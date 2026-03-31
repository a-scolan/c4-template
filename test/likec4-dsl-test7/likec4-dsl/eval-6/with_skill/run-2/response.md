Use `cloud.backend._`.

```likec4
views {
  view backend of cloud.backend {
    include cloud.backend._
  }
}
```

- `cloud.backend._` selects **only the direct children** of `cloud.backend` that have at least one relationship with the elements already accumulated in the view.
- `cloud.backend.*` would select **all direct children** of `cloud.backend`, even if some of them have no relationships with the current view result.
- `cloud.backend.**` would select **recursive descendants** of `cloud.backend` (children, grandchildren, etc.) that have relationships with the accumulated result, so it goes deeper than direct children only.
