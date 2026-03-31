```likec4
views {
  dynamic view client-orders-sequence {
    variant sequence
    client -> gateway "request" -> orders "route" -> db "query"
    orders <- db "result"
    gateway <- orders "response"
    client <- gateway "response"
  }
}
```