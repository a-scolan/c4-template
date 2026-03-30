```likec4
views {
  dynamic view checkout-flow {
    customer
      -> frontend "starts checkout"
      -> api "submits order" {
        technology 'HTTPS'
        navigateTo payment-detail
      }

    parallel {
      api -> payments "charge"
      api -> inventory "reserve"
      api -> notifications "notify"
    }
  }
}
```