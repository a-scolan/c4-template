```likec4
dynamic view client-to-db {
  title "Client to DB flow"
  variant sequence

  client -> gateway "request"
  gateway -> orders "forward"
  orders -> db "query"
  orders <- db "result"
  gateway <- orders "response"
  client <- gateway "response"
}
```

`variant sequence` renders the view as a UML sequence diagram instead of the default animated box-and-line diagram. Backward arrows (`SOURCE <- TARGET`) model response/return steps. The six steps produce the full round-trip: request downstream to `db`, responses back out to `client`.
