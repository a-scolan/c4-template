Use a dynamic view and keep the interactions in runtime order. Skeleton:
```likec4
views {
  dynamic view login_journey {
    title "Login journey"

    user -> webApp "Open sign-in page"
    user -> webApp "Submit credentials"
    webApp -> api "POST /login"
    api -> primaryDatabase "Verify user and password"
    api -> notificationService "Send login event/notification"
    api -> webApp "Return session/token"
    webApp -> user "Show logged-in state"
  }
}
```
If your repository uses a slightly different wrapper for views, keep the interaction lines as-is and adapt only the outer declaration.
