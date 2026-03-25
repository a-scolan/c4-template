```likec4
views {
  dynamic view checkout-flow {
    customer -> frontend "Start checkout" -> api "Submit checkout" {
      technology 'HTTPS'
      navigateTo payment-detail
    }

    parallel {
      api -> payments "Authorize payment"
    }
    parallel {
      api -> inventory "Reserve stock"
    }
    parallel {
      api -> notifications "Send notification"
    }
  }
}
```