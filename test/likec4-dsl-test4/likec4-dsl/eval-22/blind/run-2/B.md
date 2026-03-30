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

Rewriting the chain as separate standalone steps (`customer -> frontend` then `frontend -> api { ... }` on distinct lines) would produce two independent step expressions instead of a single chained compound expression, failing point (1).
