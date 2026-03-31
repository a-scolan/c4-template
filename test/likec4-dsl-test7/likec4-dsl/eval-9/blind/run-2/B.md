dynamic view checkout-flow {
  customer -> frontend
    -> api {
      technology 'HTTPS'
      navigateTo payment-detail
    }
  parallel {
    api -> payments
    api -> inventory
    api -> notifications
  }
}
