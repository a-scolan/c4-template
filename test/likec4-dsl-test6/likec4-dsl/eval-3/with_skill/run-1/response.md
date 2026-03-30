```likec4
dynamic view order_sequence {
  variant sequence

  client -> gateway "request"
  gateway -> orders "create order"
  orders -> db "insert order"

  orders <- db "ok"
  gateway <- orders "order created"
  client <- gateway "response"
}
```