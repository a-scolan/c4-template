```likec4
global {
  predicates {
    core-services = element.kind == 'service'
      && element.id startsWith 'cloud.'
      && !element.tag == #deprecated
  }
}

views {
  view cloud_core_services_styled of cloud {
    include @core-services

    style @core-services {
      color modern
      border dashed
    }

    autoLayout LeftRight
  }

  view cloud_core_services_with_dependencies of cloud {
    include @core-services
    include -> @core-services

    autoLayout LeftRight
  }
}
```