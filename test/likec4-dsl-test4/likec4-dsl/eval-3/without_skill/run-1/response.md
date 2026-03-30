Here is a minimal LikeC4 dynamic view snippet that renders as a UML-style sequence diagram for `client -> gateway -> orders -> db`, with response arrows back to the client:

```likec4
dynamic view ClientOrderFlow {
  title "Client Order Flow"

  // Forward arrows
  client -> gateway "1. send request"
  gateway -> orders "2. route to orders"
  orders -> db "3. query data"

  // Response arrows
  db -> orders "4. return data"
  orders -> gateway "5. return response"
  gateway -> client "6. send response"
}
```

**Key points:**

- `dynamic view` declares a dynamic (sequence-style) view in LikeC4.
- Each line inside is a step: `source -> target "label"`.
- Steps are numbered implicitly in order (or you can prefix labels manually as shown above).
- LikeC4 renders `dynamic` views as UML-style sequence diagrams by default.
- The elements (`client`, `gateway`, `orders`, `db`) must already be defined in your model (as `actor`, `system`, `container`, etc.).
