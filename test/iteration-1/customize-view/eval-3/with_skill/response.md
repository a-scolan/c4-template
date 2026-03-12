view c2_containers {
  link https://docs.internal/specs/containers 'Internal Spec Docs'

  include mySystem.webapp with {
    navigateTo c2_webapp_details
  }

  style * { color muted; opacity 40% }
  style mySystem.api { color primary; opacity 100% }
}

This skill stops at view-level styling, layout, and links; if you need to create or restructure the view itself or add a new drill-down or C3 view, hand that work to `design-view`.
