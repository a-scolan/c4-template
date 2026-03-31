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

Rewriting the chain as separate standalone steps would not satisfy the request because it would no longer test that `customer -> frontend -> api` is parsed as one chained expression with the body applying only to the `frontend -> api` hop.