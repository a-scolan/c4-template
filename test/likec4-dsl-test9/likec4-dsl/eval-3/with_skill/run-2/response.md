```likec4
views {
  dynamic view order-sequence {
    variant sequence
    client -> gateway -> orders -> db
    client <- gateway <- orders <- db
  }
}
```