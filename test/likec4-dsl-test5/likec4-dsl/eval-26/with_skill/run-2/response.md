global {
  predicateGroup core-services {
    include cloud.* where kind is service and tag is not #deprecated
  }
}

views {
  view core-services-view {
    global predicate core-services
  }
}
