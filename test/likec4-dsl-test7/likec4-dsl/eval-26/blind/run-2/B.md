```likec4
global {
  predicateGroup core-services {
    include element cloud.* where kind == service and not #deprecated
  }
}

views {
  view core of cloud {
    global predicate core-services
  }
}
```