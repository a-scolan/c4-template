```likec4
global {
  predicateGroup core-services = kind == service and id ~= 'cloud.*' and not #deprecated
}

view core of cloud {
  global predicate core-services
}
```