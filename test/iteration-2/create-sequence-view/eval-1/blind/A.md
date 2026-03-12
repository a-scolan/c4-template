Do not model `api_container -> api_container.auth_component` in a dynamic view. That is a parent calling its own child, which is the wrong shape for a time-ordered interaction view.

Show the initiating actor going straight to the participating component instead:

```likec4
views 'Use Cases' {
  dynamic view authenticationFlow {
    title 'Authentication'

    user -> api_container.auth_component 'Submit credentials'
    api_container.auth_component -> identityStore 'Validate credentials'
    api_container.auth_component -> sessionStore 'Create session'
    api_container.auth_component -> user 'Return authentication result'
  }
}
```