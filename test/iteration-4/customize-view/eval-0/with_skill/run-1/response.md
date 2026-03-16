view containers_overview {
  autoLayout LeftRight

  include user with { rank source }
  include database with { rank sink }
  include externalMailService with { rank sink }

  include webApp with {
    navigateTo webApp_details
  }
}
