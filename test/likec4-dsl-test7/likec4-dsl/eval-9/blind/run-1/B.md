```likec4
dynamic checkout-flow {
  customer -> frontend -> api {
    technology 'HTTPS'
    navigateTo payment-detail
  }

  api -> {
    payments
    inventory
    notifications
  }
}
```