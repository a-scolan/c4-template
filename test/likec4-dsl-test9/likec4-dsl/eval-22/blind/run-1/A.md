```likec4
views {
  dynamic view checkout-flow {
    customer -> frontend
      -> api {
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

Rewriting it as separate standalone steps would not satisfy the request because it would stop testing a single chained expression with a body attached only to the `frontend -> api` hop.