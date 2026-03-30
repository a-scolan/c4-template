```likec4
global {
  predicateGroup core-services {
    include cloud.* where kind is service
    exclude #deprecated
  }
}

views {
  view coreServices {
    title "Core Services"
    include global predicate core-services
  }
}
```
