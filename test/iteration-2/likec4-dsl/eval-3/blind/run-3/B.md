```likec4
dynamic view order-sequence {
  variant sequence

  client -> gateway "request"
  gateway -> orders "create order"
  orders -> db "INSERT"
  orders <- db "ok"
  gateway <- orders "201 Created"
  client <- gateway "201 Created"
}
```