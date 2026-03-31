```likec4
dynamic view sequence_orders {
  title "Client → Gateway → Orders → DB"

  client -> gateway "Request"
  gateway -> orders "Route to orders"
  orders -> db "Query/Write"

  db -> orders "Result"
  orders -> gateway "Response"
  gateway -> client "HTTP response"
}
```