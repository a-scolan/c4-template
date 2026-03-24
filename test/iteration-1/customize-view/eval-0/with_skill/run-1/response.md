views 'C2' {
  view containers_overview {
    include *

    autoLayout LeftRight

    include user with { rank source }
    include database with { rank sink }
    include mailService with { rank sink }

    include webApp with {
      navigateTo webApp_details
    }
  }
}
