views 'C2' {
  view containers_overview {
    include *

    style * { color muted; opacity 20% }
    style api.*, gateway.* { color primary; opacity 100% }

    include webApp with {
      navigateTo webApp_details
    }

    link https://docs.internal/spec 'System specification'
  }
}

This skill stops at styling, lightweight layout hints, `navigateTo`, and external links. If you need to change included elements, parent context, or create a new/detail view, hand off to `design-view`.
