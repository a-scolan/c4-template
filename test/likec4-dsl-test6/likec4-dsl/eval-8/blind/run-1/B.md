```likec4
global {
  predicateGroup core-services {
    element.kind is service
    element.id startsWith 'cloud.'
    not element.tag is #deprecated
  }
}

views {
  view cloud_core_styled of cloud {
    global predicate core-services

    style element.tag is #critical {
      color red
      border solid
    }
  }

  view cloud_core_plus_extra of cloud {
    global predicate core-services
    include cloud.billing
  }
}
```