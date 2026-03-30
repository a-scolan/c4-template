```likec4
dynamic view checkout-sequence {
  variant sequence

  client -> gateway "request"
  gateway -> orders "create order"
  orders -> db "write"

  orders <- db "ok"
  gateway <- orders "created"
  client <- gateway "response"
}
```