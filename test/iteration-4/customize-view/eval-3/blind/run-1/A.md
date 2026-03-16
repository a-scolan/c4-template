view containers_overview {
  style * { color muted; opacity 20% }
  style api, api.* { color primary; opacity 100% }

  include webApp with {
    navigateTo webApp_details
  }

  link https://docs.internal/spec Internal specification
}

This skill stops at styling, layout hints, navigation, and external links. If you need to change included elements, parent context, or create a new view, hand off to design-view.
