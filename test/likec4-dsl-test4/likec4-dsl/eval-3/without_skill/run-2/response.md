Here is a minimal LikeC4 dynamic view snippet that renders as a UML-style sequence for `client -> gateway -> orders -> db` with response arrows back to the client:

```likec4
dynamic view OrderFlow {
  title "Order Flow Sequence"

  client -> gateway "send request"
  gateway -> orders "forward request"
  orders -> db "query data"
  db -> orders "return data"
  orders -> gateway "return response"
  gateway -> client "send response"
}
```

**Key points:**

- `dynamic view` is the LikeC4 view type that renders as a sequence diagram (UML-style).
- Each step is written as `source -> target "label"`.
- The forward path (`client -> gateway -> orders -> db`) and the return path (`db -> orders -> gateway -> client`) are listed in order — LikeC4 numbers them automatically.
- The elements (`client`, `gateway`, `orders`, `db`) must be defined elsewhere in the model (e.g. as `actor`, `system`, `container`, or `component` elements).

If those elements are in a namespace, use their fully-qualified names, e.g. `shop.client`, `shop.gateway`, etc.
