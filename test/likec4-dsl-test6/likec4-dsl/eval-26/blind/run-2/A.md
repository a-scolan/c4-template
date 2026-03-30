```likec4
global {
  predicateGroup core-services {
    include cloud.* where kind is service
    exclude * where tag is #deprecated
  }
}

views {
  view services {
    global predicate core-services
  }
}
```