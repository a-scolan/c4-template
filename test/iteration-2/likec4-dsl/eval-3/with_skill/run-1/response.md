```likec4
dynamic view order-flow {
  title "Order Request Flow"
  variant sequence

  client -> gateway "send request"
  gateway -> orders "route request"
  orders -> db "query"
  orders <- db "return results"
  gateway <- orders "return response"
  client <- gateway "send response"
}
```

Key points:
- `variant sequence` switches rendering to UML-style sequence diagram.
- Forward steps use `->`, response (return) steps use `<-` (source receives from target).
- Steps are listed in execution order; LikeC4 assigns step numbers automatically.
- Elements (`client`, `gateway`, `orders`, `db`) must already exist in the model.
