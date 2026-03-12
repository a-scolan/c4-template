Use a dynamic view in `views 'Use Cases'` and keep every interaction as a plain time-ordered `->` step.

```likec4
views 'Use Cases' {
  dynamic view loginJourney {
    title 'Login Journey'

    user -> webApp 'Open login page'
    user -> webApp 'Submit credentials'
    webApp -> api 'Send login request'
    api -> primaryDatabase 'Load account and credential data'
    api -> notificationService 'Send login alert'
    api -> webApp 'Return authentication result'
    webApp -> user 'Show signed-in state'
  }
}
```