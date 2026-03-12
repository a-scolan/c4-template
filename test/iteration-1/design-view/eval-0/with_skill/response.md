Place the overview inside `views 'C2'` and let the web application drill down to a dedicated detail view.

```likec4
views 'C2' {
  view c2_containers {
    title 'Containers'

    // Parent context
    include mySystem

    // Focus
    include mySystem.*

    // Neighboring context
    include user
    include emailService
    include -> mySystem.*
    include mySystem.* ->

    // Drill-down from the webapp
    include mySystem.webapp with {
      navigateTo c3_webapp
    }

    rank source { user }
    rank sink { mySystem.database, emailService }
  }
}

views 'C3' {
  view c3_webapp {
    title 'Web Application'

    include mySystem.webapp
    include -> mySystem.webapp
    include mySystem.webapp ->
  }
}
```

This keeps the C2 view in the right folder, shows the parent `mySystem`, includes the focused containers via `mySystem.*`, and preserves interaction context with the user, `emailService`, and relationship-based neighbors.
