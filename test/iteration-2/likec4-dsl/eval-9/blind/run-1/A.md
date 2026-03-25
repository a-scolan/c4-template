```likec4
views {
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
}
```

Key points:
- `customer -> frontend -> api { ... }` is a single chained expression; the body block attaches to the last arrow (`frontend -> api`).
- `technology` and `navigateTo` are valid relationship properties inside any step body.
- `parallel { ... }` (or `par { ... }`) groups simultaneous fan-out steps; each line inside is an independent step rendered in parallel.
