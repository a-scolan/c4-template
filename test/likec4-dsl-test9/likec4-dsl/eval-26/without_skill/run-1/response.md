```likec4
global {
  predicateGroup core-services {
    include cloud.* and kind service
    exclude #deprecated
  }
}

view of cloud {
  global predicate core-services
}
```