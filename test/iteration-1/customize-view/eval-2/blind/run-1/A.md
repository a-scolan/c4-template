views 'C2' {
  view containers_overview {
    include *

    include webApp with {
      navigateTo webApp_details
    }

    link https://docs.internal/spec 'System specification'
  }
}
