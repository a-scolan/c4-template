```likec4
global {
  predicateGroup core-services {
    include cloud.*
    where kind == 'service' and not tag == '#deprecated'
  }
}

views {
  view coreServicesStyled of cloud {
    global predicate core-services

    style {
      element "*" {
        color "#1d4ed8"
        border dashed
      }
    }
  }

  view coreServicesWithExtraInclude of cloud {
    global predicate core-services
    include cloud.shared.logging
  }
}
```