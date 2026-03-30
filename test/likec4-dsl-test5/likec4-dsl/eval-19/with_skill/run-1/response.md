- Base include set: in a scoped view `of cloud.backend`, `include *` includes `cloud.backend` and its **direct children**.
- Additional visibility: relationships connected to that scoped include set can bring neighboring context into view, and explicit relationship predicates can add incoming/outgoing edges (and their endpoints) around `cloud.backend`.

```likec4
view backend of cloud.backend {
  include *
  include -> cloud.backend ->
}
```
