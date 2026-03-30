```likec4
dynamic view checkout-flow {
  customer -> frontend -> api {
    technology 'HTTPS'
    navigateTo payment-detail
  }
  parallel {
    api -> payments
    api -> inventory
    api -> notifications
  }
}
```

**How each requirement is met:**

1. **Chained step syntax** — `customer -> frontend -> api { ... }` is a single compound chain expression. The body `{ ... }` is attached to the last hop (`frontend -> api`), not written as three separate `->` lines.

2. **Body on `frontend -> api`** — `technology 'HTTPS'` and `navigateTo payment-detail` are placed in the block that follows `api` in the chain, targeting that last hop.

3. **Parallel fanout** — `parallel { ... }` groups the three independent `api ->` steps so they are rendered as simultaneous outgoing arrows from `api` to `payments`, `inventory`, and `notifications`.
