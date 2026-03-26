Yes—this is a dynamic sequence, so place it in `views 'Use Cases'`.

```likec4
views 'Use Cases' {
  dynamic view userLoginFlow {
    title 'User Login Flow'
    user -> webApplication 'Starts sign-in'
    webApplication -> api 'Submit credentials'
    api -> primaryDatabase 'Checks user/password'
    api -> externalNotificationService 'Publishes login event'
    api -> webApplication 'Auth result + token'
    webApplication -> user 'Redirects to dashboard'
  }
}
```

Critical anti-pattern: avoid modeling parent-to-own-child calls in dynamic steps.
Yes—this is a dynamic sequence, so place it in `views 'Use Cases'`.

```likec4
views 'Use Cases' {
  dynamic view userLoginFlow {
    title 'User Login Flow'
    user -> webApplication 'Starts sign-in'
    webApplication -> api 'Submit credentials'
    api -> primaryDatabase 'Checks user/password'
    api -> externalNotificationService 'Publishes login event'
    api -> webApplication 'Auth result + token'
    webApplication -> user 'Redirects to dashboard'
  }
}
```

Critical anti-pattern: avoid modeling parent-to-own-child calls in dynamic steps.
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
