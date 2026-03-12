Add a use-case dynamic view like this:

```likec4
views 'Use Cases' {
  dynamic view login_journey {
    title 'Login'

    user -> mySystem.webapp 'Opens the login page'
    mySystem.webapp -> mySystem.api 'Submits credentials'
    mySystem.api -> mySystem.database 'Loads account data'
    mySystem.api -> emailService 'Sends verification or notification email'
    mySystem.api -> mySystem.webapp 'Returns authentication result'
    mySystem.webapp -> user 'Shows the signed-in state'
  }
}
```

This keeps the flow in temporal order, starts with `user`, and uses only plain `->` arrows with action labels.
