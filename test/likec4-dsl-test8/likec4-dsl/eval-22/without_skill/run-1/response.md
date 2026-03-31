```likec4
dynamic view checkout-flow {
  customer -> frontend -> api {
    technology 'HTTPS'
    navigateTo payment-detail
  }

  api -> parallel {
    payments
    inventory
    notifications
  }
}
```

Rewriting the chain as separate standalone steps would not satisfy the request because it would no longer test that `customer -> frontend -> api` is expressed as one single chained expression with the body attached only to the `frontend -> api` hop.