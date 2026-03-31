```likec4
global {
  predicateGroup core-services {
    include cloud.* where kind is service
    exclude * where tag is #deprecated
  }
}

views {
  view core-services-styled {
    global predicate core-services

    // Per-view style rule layered on top of the reusable predicate
    style cloud.* { color primary }
  }

  view core-services-with-extra-include {
    global predicate core-services

    // Extra include rule layered on top of the reusable predicate
    include -> cloud.*
  }
}
```