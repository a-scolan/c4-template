```likec4
global {
  predicates {
    core-services = kind is service and element is cloud.* and tag is not #deprecated
  }
}

view core-a {
  include @core-services
  style @core-services {
    color blue
  }
}

view core-b {
  include @core-services
  include cloud.gateway
}
```