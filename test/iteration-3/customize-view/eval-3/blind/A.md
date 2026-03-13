view containers_overview {
  style * { color muted; opacity 25% }
  style api, api.* { color primary; opacity 100% }

  include webApp with {
    navigateTo webApp_details
  }

  link https://docs.internal/specs/container-view 'Internal container docs'
}

This skill stops at view polish: style, light layout hints, navigateTo, and external links. If the web application detail view does not already exist, or if you need to change includes, parent context, or neighbors, hand that off to design-view.
