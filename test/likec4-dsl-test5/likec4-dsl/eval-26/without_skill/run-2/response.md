```c4
global {
  predicateGroup core-services {
    include cloud.*
    where kind == service
    exclude #deprecated
  }
}

view core of cloud {
  global predicate core-services
}
``````likec4
global {
  predicateGroup core-services {
    include cloud.* where kind == service
    exclude #deprecated
  }
}

views {
  view services_overview {
    title "Core Services Overview"
    global predicate core-services
  }
}
```
