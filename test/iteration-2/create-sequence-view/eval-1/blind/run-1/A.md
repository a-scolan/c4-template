`api_container -> api_container.auth_component` is the wrong pattern for a dynamic view.

Why to avoid it:
- It mixes hierarchy levels in a single interaction step (parent container directly calling its own child component).
- Dynamic views should show message flow between explicitly participating elements at the same modeling level for that scenario.

Use one of these corrected approaches:

1) **Container-level dynamic view** (no internal component call shown)
```likec4
dynamicView auth_container_flow {
  include webApp
  include api_container
  include identityProvider

  webApp -> api_container "POST /login"
  api_container -> identityProvider "Validate credentials"
  identityProvider -> api_container "Auth result"
  api_container -> webApp "Token / error"
}
```

2) **Component-level dynamic view** (show auth component explicitly)
```likec4
dynamicView auth_component_flow {
  include api_container.login_controller
  include api_container.auth_component
  include identityProvider

  api_container.login_controller -> api_container.auth_component "Authenticate(user, pass)"
  api_container.auth_component -> identityProvider "Validate credentials"
  identityProvider -> api_container.auth_component "Auth result"
  api_container.auth_component -> api_container.login_controller "Token / error"
}
```

So: keep each dynamic view scoped consistently (container-to-container or component-to-component), instead of parent-to-child messaging.