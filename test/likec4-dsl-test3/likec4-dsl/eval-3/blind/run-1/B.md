```likec4
dynamic view seq_client_gateway_orders_db {
  client -> gateway "request"
  gateway -> orders "forward"
  orders -> db "query"

  db -> orders "result"
  orders -> gateway "response"
  gateway -> client "response"
}
```