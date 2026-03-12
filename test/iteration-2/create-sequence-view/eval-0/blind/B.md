Use a dynamic view under `views 'Use Cases'`, start from the initiating actor, and keep every interaction as a plain `->` step with an action label.

```likec4
views 'Use Cases' {
  dynamic view login_journey {
    title 'Login Journey'

    user -> webApplication 'Opens login form and submits credentials'
    webApplication -> api 'POST /login'
    api -> primaryDatabase 'Validate credentials and load user record'
    api -> externalNotificationService 'Send login notification'
    api -> webApplication 'Return authenticated session'
    webApplication -> user 'Show signed-in experience'
  }
}
```

If your real element IDs differ, just replace `webApplication`, `api`, `primaryDatabase`, and `externalNotificationService` with the actual model names.