```likec4
dynamic view checkout-flow {
  customer -> frontend "checkout" -> api "create order" {
    technology 'HTTPS'
    navigateTo payment-detail
  }

  parallel {
    api -> payments "authorize"
    api -> inventory "reserve"
    api -> notifications "notify"
  }
}
```

Rewriting this as separate standalone steps would violate the requirement to express `customer -> frontend -> api` as one chained expression.