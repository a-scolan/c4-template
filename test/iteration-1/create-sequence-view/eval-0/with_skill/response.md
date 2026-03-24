Yes — this belongs in `views 'Use Cases'`.

views 'Use Cases' {
  dynamic view loginJourney {
    title 'Login Journey'
    user -> webApp 'Opens login'
    webApp -> api 'POST /login'
    api -> primaryDatabase 'Checks credentials'
    api -> externalNotificationService 'Sends login alert'
    api -> webApp 'Returns session'
  }
}

Keep labels short and action-focused. One anti-pattern to avoid: `webApp -> webApp.someChild` inside the dynamic view.
