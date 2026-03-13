This belongs in `views 'Use Cases'`.

views 'Use Cases' {
  dynamic view loginJourney {
    title 'Login Journey'
    user -> webApp 'Opens sign-in'
    webApp -> api 'Submits credentials'
    api -> primaryDatabase 'Validates account'
    api -> externalNotificationService 'Sends login alert'
    api -> webApp 'Returns authenticated session'
    webApp -> user 'Shows signed-in state'
  }
}

Anti-pattern to avoid: do not switch to model-style arrows such as `user -[uses]-> webApp`; in a dynamic view, keep plain `->` arrows only.
