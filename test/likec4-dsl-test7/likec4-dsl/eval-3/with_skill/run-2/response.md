```likec4
views {
  dynamic view request-flow {
    variant sequence
    client -> gateway -> orders -> db
    client <- gateway <- orders <- db
  }
}
```