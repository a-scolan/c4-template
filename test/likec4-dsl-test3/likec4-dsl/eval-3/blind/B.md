```likec4
dynamic view client_gateway_orders_db_seq {
  client  -> gateway "Request"
  gateway -> orders  "Forward request"
  orders  -> db      "Query/Write"

  db      -> orders  "Result"
  orders  -> gateway "Response"
  gateway -> client  "HTTP response"
}
```