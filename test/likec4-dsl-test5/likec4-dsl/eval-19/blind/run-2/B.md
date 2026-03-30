- In a scoped view, `include *` starts from the scoped element (`cloud.backend`) plus its **direct children** as the base include set.
- From that base, additional neighboring context can still appear via relationship predicates (for example incoming/outgoing links), which may bring connected elements/edges into the rendered view.

```likec4
views {
  view backend of cloud.backend {
    include *
    include -> cloud.backend
    include cloud.backend ->
  }
}
```