```likec4
dynamic view checkout-flow {
  customer -> frontend "Start checkout" -> api "Submit checkout" {
    technology 'HTTPS'
    navigateTo payment-detail
  }

  parallel {
    api -> payments "Authorize payment"
    api -> inventory "Reserve stock"
    api -> notifications "Send notification"
  }
}
```