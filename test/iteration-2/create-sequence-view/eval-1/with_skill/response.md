That `api_container -> api_container.auth_component` pattern should not be used in a dynamic view.

A dynamic view shows interactions between participants over time, and it must not model a parent element calling its own child. In other words, avoid `parent -> own-child` such as `api_container -> api_container.auth_component`.

The fix is to target the component directly from the real initiating actor or caller.

```likec4
views 'Use Cases' {
  dynamic view authentication_flow {
    title 'Authentication'

    user -> auth_component 'Submits credentials'
    auth_component -> primaryDatabase 'Validate credentials'
    auth_component -> notificationService 'Send login alert'
    auth_component -> user 'Return authentication result'
  }
}
```

If the web app is the caller in your model, that is also fine:

```likec4
views 'Use Cases' {
  dynamic view authentication_flow {
    title 'Authentication'

    user -> webApp 'Starts sign-in'
    webApp -> auth_component 'POST /login'
    auth_component -> primaryDatabase 'Validate credentials'
    auth_component -> webApp 'Return auth result'
    webApp -> user 'Show signed-in state'
  }
}
```

The key correction is the same in both versions: the actor or external caller addresses `auth_component` directly, and the view stays in `views 'Use Cases'` with simple `->` arrows only.