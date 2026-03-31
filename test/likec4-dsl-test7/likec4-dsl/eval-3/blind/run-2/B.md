```likec4
dynamic "Client orders flow" {
  client -> gateway "request"
  gateway -> orders "create order"
  orders -> db "insert"

  db -> orders "ok"
  orders -> gateway "created"
  gateway -> client "201 Created"
}
```