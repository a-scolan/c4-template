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

Rewriting the chain as separate standalone steps would not satisfy the request because it explicitly requires `customer -> frontend -> api` to stay a single chained expression, with the body attached only to the `frontend -> api` hop.