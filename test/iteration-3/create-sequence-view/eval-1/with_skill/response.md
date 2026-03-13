`api_container -> api_container.auth_component` is the wrong shape for a dynamic view because it shows `parent -> own-child`, and that should not be modeled in the sequence.

A better correction is to have the initiating actor target the component directly:

views 'Use Cases' {
  dynamic view authenticationFlow {
    title 'Authentication Flow'
    user -> api_container.auth_component 'Submits credentials'
  }
}

If you need more steps, continue from `api_container.auth_component` to peer or external elements with plain `->` arrows, but do not keep `api_container -> api_container.auth_component`.
