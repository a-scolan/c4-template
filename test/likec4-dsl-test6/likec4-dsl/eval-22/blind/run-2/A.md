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

Rewriting the chain as separate standalone steps would fail the request because it would no longer model `customer -> frontend -> api` as one chained expression with the body attached only to the `frontend -> api` hop.