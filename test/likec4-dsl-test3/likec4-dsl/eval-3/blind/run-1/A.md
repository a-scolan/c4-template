```likec4
views {
  dynamic view request-flow {
    variant sequence

    client -> gateway "Request"
    gateway -> orders "Forward request"
    orders -> db "Query/Write"

    db <- orders "Result"
    orders <- gateway "Response"
    gateway <- client "Response"
  }
}
```