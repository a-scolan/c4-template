dynamic view checkout-flow {
  customer
    -> frontend 'checkout'
    -> api 'submit order' {
      technology 'HTTPS'
      navigateTo payment-detail
    }

  parallel {
    api -> payments 'charge'
    api -> inventory 'reserve'
    api -> notifications 'notify'
  }
}
