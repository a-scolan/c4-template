# Minimal LikeC4 dynamic view snippet

```likec4
dynamic view client_gateway_orders_db {
  title "Client → Gateway → Orders → DB"

  client -> gateway "Request"
  gateway -> orders "Forward request"
  orders -> db "Query"

  db -> orders "Result"
  orders -> gateway "Response"
  gateway -> client "HTTP 200"
}
```

This is the smallest dynamic-view style snippet showing the forward request chain and the response arrows all the way back to `client`.
