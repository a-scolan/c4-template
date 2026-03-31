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

Rewriting the chain as separate standalone steps would not satisfy the request because it would stop testing the required single chained expression and the hop-local body would no longer be attached specifically to only the `frontend -> api` hop.
