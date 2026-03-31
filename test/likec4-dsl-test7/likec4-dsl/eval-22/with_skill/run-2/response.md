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

Rewriting the chain as separate standalone steps would fail the request because `customer -> frontend -> api` must remain one chained expression, with the body scoped only to the `frontend -> api` hop inside that single chain.