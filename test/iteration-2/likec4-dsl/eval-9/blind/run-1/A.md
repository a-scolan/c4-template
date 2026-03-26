```likec4
dynamic view checkout-flow {
  customer
    -> frontend "opens checkout"
    -> api "POST /checkout" {
      technology "HTTPS"
      navigateTo payment-detail
    }

  parallel {
    api -> payments "charge"
    api -> inventory "reserve"
    api -> notifications "notify"
  }
}
```