```likec4
global {
  predicateGroup core-services {
    include cloud.* where kind is service
    exclude * where tag is #deprecated
  }
}

views {
  view services-styled {
    global predicate core-services
    style * { color primary }
  }

  view services-with-extra-include {
    global predicate core-services
    include -> cloud.*
  }
}
```