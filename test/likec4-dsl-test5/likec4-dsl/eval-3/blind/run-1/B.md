```likec4
dynamic view request-sequence {
  variant sequence

  client -> gateway "request"
  gateway -> orders "create order"
  orders -> db "write"

  orders <- db "ok"
  gateway <- orders "ok"
  client <- gateway "ok"
}
```