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

Rewriting this as separate standalone steps would violate the requirement to express `customer -> frontend -> api` as one chained expression with the body attached only to the `frontend -> api` hop.