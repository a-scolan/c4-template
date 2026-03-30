```c4
global {
  predicateGroup core-services {
    include cloud.* where kind is service
    exclude #deprecated
  }
}

views {
  view coreServicesView {
    title "Core Services"
    global predicate core-services
  }
}
```
