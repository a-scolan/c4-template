Using the repo's naming/style (`Actor_Person`, `Container_Webapp`, `Container_Api`, `Container_Database`, `System_External`), a minimal LikeC4 dynamic-view skeleton is:
views 'Use Cases' {
  dynamic view login_journey {
    title 'Login Journey'

    include user
    include mySystem.webapp
    include mySystem.api
    include mySystem.database
    include notificationService

    user -> mySystem.webapp 'Enter credentials'
    mySystem.webapp -> mySystem.api 'POST /login'
    mySystem.api -> mySystem.database 'Load user and verify password'
    mySystem.api -> notificationService 'Send login notification'
    mySystem.api -> mySystem.webapp 'Return session/token'
    mySystem.webapp -> user 'Show logged-in state'
  }
}

Model the static relationships first with `calls`, `reads`, and `writes`, then use the dynamic view only to show the order of interactions.
