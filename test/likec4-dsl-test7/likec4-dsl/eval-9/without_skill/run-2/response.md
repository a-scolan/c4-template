```likec4
dynamic view checkout-flow {
  customer -> frontend -> api {
    technology 'HTTPS'
    navigateTo payment-detail
  }

  parallel {
    api -> payments
  } and {
    api -> inventory
  } and {
    api -> notifications
  }
}
```