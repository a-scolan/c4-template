A good LikeC4 dynamic-view skeleton for this login journey is:

```likec4
dynamicView login_journey {
  title "Login journey"
  description "User logs in via web app; API verifies credentials; DB is queried; notification is sent externally."

  include externalUser
  include webApplication
  include api
  include primaryDatabase
  include externalNotificationService

  externalUser -> webApplication "Enter credentials"
  webApplication -> api "POST /login"
  api -> primaryDatabase "Validate user + password hash"
  primaryDatabase -> api "User record / auth result"
  api -> externalNotificationService "Send login notification"
  api -> webApplication "Login success + session/token"
  webApplication -> externalUser "Show logged-in state"
}
```

If you later need alternatives (invalid password, MFA, lockout), model each as a separate dynamic view instead of branching heavily in one view.