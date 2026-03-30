```likec4
global {
  predicateGroup core-services {
    include cloud.* where kind == 'service' and !#deprecated
  }
}

view services of cloud {
  global predicate core-services
}
```
```likec4
global {
  predicateGroup core-services {
    include cloud.* where kind is service
    exclude #deprecated
  }
}

views {
  view cloud_services of cloud {
    global predicate core-services
  }
}
```
