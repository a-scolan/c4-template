```likec4
global {
  predicateGroup core-services {
    include cloud.* where kind == service
    exclude #deprecated
  }
}

views {
  view coreServices of cloud {
    global predicate core-services
  }
}
```