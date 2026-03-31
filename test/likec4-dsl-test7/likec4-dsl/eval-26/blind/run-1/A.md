```c4
global {
  predicateGroup core-services {
    include cloud.* where kind == service and not #deprecated
  }
}

view core-services-view {
  include *
  global predicate core-services
}
```