```likec4
global {
  predicateGroup core-services {
    include element.kind == 'service' and element.id startsWith 'cloud.'
    exclude #deprecated
  }
}

view cloud-core-with-style of cloud {
  global predicate core-services

  style {
    element.kind == 'service' {
      color '#2F80ED'
      border dashed
    }
  }
}

view cloud-core-with-include of cloud {
  global predicate core-services

  include cloud.gateway
}
```