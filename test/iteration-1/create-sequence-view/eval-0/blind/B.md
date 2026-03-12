For `projects/template/system-views.c4`, add a dedicated use-case view like this:

```likec4
views 'Use Cases' {
  dynamic view login_journey of mySystem {
    title 'Login Journey'

    include user
    include mySystem.webapp
    include mySystem.api
    include mySystem.database
    include emailService

    user -> mySystem.webapp 'Enters email and password'
    mySystem.webapp -> mySystem.api 'Submits login request'
    mySystem.api -> mySystem.database 'Loads account and password hash'
    mySystem.api -> emailService 'Sends login notification'
    mySystem.api -> mySystem.webapp 'Returns authenticated session'
    mySystem.webapp -> user 'Shows signed-in state'
  }
}
```

This keeps the sequence actor-first and uses only simple `->` steps with action labels.
