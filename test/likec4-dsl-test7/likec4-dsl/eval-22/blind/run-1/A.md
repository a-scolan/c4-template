```likec4
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
```

Rewriting the chain as separate standalone steps would fail the request because it explicitly requires `customer -> frontend -> api` to remain one chained expression while the body applies only to the `frontend -> api` hop.
