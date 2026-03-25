```likec4
global {
  predicates {
    core-services = element.kind == service and element.id like 'cloud.*' and not (element.tag == #deprecated)
  }
}

views {
  view core_services_styled {
    title 'Core services (styled)'
    include * where @core-services

    style {
      element where @core-services {
        color blue
        border solid
      }
    }

    autoLayout TopBottom
  }

  view core_services_with_extra_include {
    title 'Core services (+ extra include)'
    include * where @core-services
    include cloud.shared-auth

    autoLayout LeftRight
  }
}
```