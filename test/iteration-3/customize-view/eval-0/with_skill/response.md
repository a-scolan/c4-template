view containers_overview {
  autoLayout LeftRight

  include user with { rank source }

  include user -> webApp ->
  include -> database
  include webApp -> mailService

  include webApp with {
    navigateTo webApp_details
  }
}
