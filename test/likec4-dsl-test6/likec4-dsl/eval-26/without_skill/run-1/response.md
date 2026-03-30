```likec4
global {
  predicateGroup core-services {
    include cloud.* where kind == 'service' and not #deprecated
  }
}

view coreServices of cloud {
  global predicate core-services
}
```