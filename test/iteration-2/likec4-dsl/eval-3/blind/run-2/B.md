```likec4
dynamic view request-flow {
  client -> gateway -> orders -> db
  db -> orders -> gateway -> client
}
```