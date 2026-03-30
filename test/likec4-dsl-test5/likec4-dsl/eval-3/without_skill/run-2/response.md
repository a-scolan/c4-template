```likec4
dynamic client_gateway_orders_db {
  title "Client → Gateway → Orders → DB"

  client -> gateway "request"
  gateway -> orders "forward"
  orders -> db "query/write"

  db --> orders "result"
  orders --> gateway "response"
  gateway --> client "response"
}
```# Minimal LikeC4 Dynamic View – Sequence Diagram

```likec4
dynamic view sequence_order_flow {
  title "Order Request Flow"

  client -> gateway "Send request"
  gateway -> orders  "Route to Orders service"
  orders  -> db      "Query database"
  db      -> orders  "Return results"
  orders  -> gateway "Return response"
  gateway -> client  "Send response"

  autoLayout TopBottom
}
```

## Notes

- `dynamic view` is the LikeC4 construct that produces a UML-style sequence diagram when `autoLayout TopBottom` (or no manual layout) is used together with sequence rendering.
- Each `->` step becomes a numbered arrow in the sequence; the direction of the arrow determines the flow.
- Response arrows are simply additional steps with reversed source/target.
- All referenced identifiers (`client`, `gateway`, `orders`, `db`) must already be declared as elements in the model (e.g. `actor`, `system`, `container`, `component`).
