Put the reusable predicate in the project-level global block, then reference it from each view. A concise example is:

global {
  predicates {
    core-services = kind == service and id like "cloud.*" and not #deprecated
  }
}

views {
  view core-services-styled of cloud {
    include core-services

    style core-services {
      color "#2F6FEB"
      border dashed
    }
  }

  view core-services-plus-extra of cloud {
    include core-services
    include cloud.gateway
  }
}

This gives you one reusable predicate group (`core-services`) in `global { predicates { ... } }`, one view that layers a per-view style on top of that group, and a second view that reuses the same group but adds one more `include` rule.
