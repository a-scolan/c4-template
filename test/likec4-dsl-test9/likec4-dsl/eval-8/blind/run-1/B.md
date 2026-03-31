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
    style cloud.* { color primary }
  }

  view core-services-expanded {
    global predicate core-services
    include * -> cloud.*
  }
}
```