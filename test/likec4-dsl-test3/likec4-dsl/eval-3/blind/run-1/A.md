```likec4
dynamic view client-orders-sequence {
  variant sequence

  client -> gateway "Request"
  gateway -> orders "Place order"
  orders -> db "Write order"

  db <- orders "Ack"
  orders <- gateway "Order result"
  gateway <- client "Response"
}
```