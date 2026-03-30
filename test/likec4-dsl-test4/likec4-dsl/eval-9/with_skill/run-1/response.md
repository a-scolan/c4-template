```likec4
dynamic view checkout-flow {
  title "Checkout Flow"

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

- **Chained expression** — `customer -> frontend -> api` is a single compound step (two hops written as one expression). The body `{ ... }` attaches to the last arrow, making it the body of the `frontend -> api` step.
- **Body on `frontend -> api`** — `technology 'HTTPS'` and `navigateTo payment-detail` are both valid relationship-step properties placed inside the body of that final hop.
- **Parallel fan-out** — after the chain, `parallel { ... }` emits all three outgoing steps from `api` simultaneously, rendering them as concurrent branches in the sequence or flow diagram.
