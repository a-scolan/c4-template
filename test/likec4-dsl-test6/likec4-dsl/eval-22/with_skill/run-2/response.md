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

Rewriting it as separate standalone steps would no longer satisfy the requirement to test the chained-step syntax in a single `customer -> frontend -> api` expression.