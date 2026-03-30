```likec4
dynamic view checkout-flow {
  customer
    -> frontend
    -> api {
      technology "HTTPS"
      navigateTo payment-detail
    }

  parallel {
    api -> payments
    api -> inventory
    api -> notifications
  }
}
```

Rewriting it as separate standalone steps would fail the requirement that `customer -> frontend -> api` be expressed as one chained expression with the body attached only to the `frontend -> api` hop.