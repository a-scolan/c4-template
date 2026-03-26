In `view backend of cloud.backend`, `include *` means: include the scoped element (`cloud.backend`) + its direct children + relationships with them. It does **not** include the whole model.

```likec4
view backend of cloud.backend {
  include *
  include -> cloud.backend ->
}
```

`-> cloud.backend ->` adds incoming and outgoing relationships between `cloud.backend` and already-accumulated context.