link 'https://intranet.example/specs/c2-containers'

include mySystem.webapp with {
  navigateTo c2_webapp_details
}

include * where tag is not #Api with {
  style {
    opacity 25%
  }
}

This stops at view-scoped customization on an existing model: emphasis, layout hints, drill-down, and external docs links. It does not create or rename model elements, add relationships, or invent a new detail view.
