```likec4
views {
  dynamic view request_flow {
    variant sequence

    client -> gateway "Request"
    gateway -> orders "Forward request"
    orders -> db "Query"
    orders <- db "Rows"
    gateway <- orders "Response"
    client <- gateway "Response"
  }
}
```