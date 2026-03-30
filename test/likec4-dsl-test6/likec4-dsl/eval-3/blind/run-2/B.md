```likec4
dynamic view client_gateway_orders_db {
  title "Client -> Gateway -> Orders -> DB"

  client -> gateway "Request"
  gateway -> orders "Forward request"
  orders -> db "Write/read data"

  db --> orders "Result"
  orders --> gateway "Response"
  gateway --> client "HTTP response"
}
```

This is the minimal dynamic-view pattern for a UML-style sequence: forward arrows down the call chain, then return arrows back out to the client.