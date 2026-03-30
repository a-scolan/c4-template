I have this base view:
```likec4
view backend-overview of cloud.backend {
  include *
}
```
Write a `detail` view that: (1) extends `backend-overview`, (2) adds just `include api` — relying on scope inheritance so I don't need the full FQN `cloud.backend.api`, and (3) adds all incoming relationships to `cloud.backend` from the rest of the model using a relationship predicate. Show the DSL and explain what scope inheritance means here.
