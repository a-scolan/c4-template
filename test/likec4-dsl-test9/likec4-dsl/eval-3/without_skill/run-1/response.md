A minimal LikeC4 dynamic view snippet could look like this:

```likec4
model {
  person client
  system gateway
  system orders
  system db

  client -> gateway "Request"
  gateway -> orders "Forward request"
  orders -> db "Query / write"
}

views {
  dynamic client_to_db_sequence {
    title "Client to DB sequence"

    client -> gateway "Request"
    gateway -> orders "Forward request"
    orders -> db "Query / write"
    db -> orders "Result"
    orders -> gateway "Response"
    gateway -> client "HTTP 200"
  }
}
```

If your model elements already exist elsewhere, keep only the `dynamic` view block and reuse those existing element ids.