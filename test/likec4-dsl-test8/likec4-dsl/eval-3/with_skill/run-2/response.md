```likec4
views {
  dynamic view request-sequence {
    variant sequence
    client -> gateway -> orders -> db
    client <- gateway <- orders <- db
  }
}
```