Do not model `api_container -> api_container.auth_component` in a dynamic view. A dynamic view shows interactions between participants, not a parent calling its own child. Keep the container/component hierarchy in the static C3 view, and let the initiating actor target the component directly.

```likec4
views 'Use Cases' {
  dynamic view authentication_flow {
    title 'Authentication'

    person_external -> api_container.auth_component 'Submits credentials'
    api_container.auth_component -> component_database 'Loads user record'
    api_container.auth_component -> person_external 'Returns authentication result'
  }
}
```
