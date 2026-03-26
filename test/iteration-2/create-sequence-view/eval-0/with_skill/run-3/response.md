Great candidate for a dynamic view under `views 'Use Cases'`.

```likec4
views 'Use Cases' {
  dynamic view loginFlow {
    title 'Login Flow'
    user -> webApplication 'Enters credentials'
    webApplication -> api 'POST /auth/login'
    api -> primaryDatabase 'Verifies account'
    api -> externalNotificationService 'Triggers login alert'
    api -> webApplication 'Returns JWT/session'
    webApplication -> user 'Displays authenticated home'
  }
}
```

One anti-pattern to avoid: parent calling its own child directly in the dynamic flow.
## Login Journey – Dynamic View

This flow belongs in `views 'Use Cases'`.

```likec4
views 'Use Cases' {
  dynamic view loginFlow {
    title 'Login Journey'
    user -> webApp 'Opens login page'
    webApp -> api 'POST /auth/login'
    api -> primaryDatabase 'Validates credentials'
    api -> webApp 'Returns auth token'
    webApp -> user 'Redirects to dashboard'
    api -> notificationService 'Sends login notification'
  }
}
```

**Notes:**
- Start with the initiating actor (`user`).
- Use plain `->` arrows — not relationship-kind syntax like `-[calls]->`.
- Labels are short and action-focused.
- The notification to `notificationService` is placed after the token is returned, reflecting a post-login side-effect.

**Anti-pattern to avoid:**
```likec4
// ❌ Wrong: parent → own-child
webApp -> webApp.loginForm 'Shows form'

// ✅ Better: reference the child directly
user -> webApp.loginForm 'Fills login form'
```
