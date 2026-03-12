Add this inside `views 'C2'` in `projects/template/system-views.c4`:

```likec4
view c2_mySystem {
  title 'My System - Containers'

  // Parent system
  include mySystem

  // Neighboring context
  include user
  include emailService

  // Container focus
  include mySystem.*

  include mySystem.webapp with {
    navigateTo c2_webapp_details
  }

  rank source { user }
  rank sink { mySystem.database, emailService }
}
```

This keeps `mySystem` as the parent context, `mySystem.*` as the focus, and `user` plus `emailService` as the neighboring context, while preserving drill-down from `mySystem.webapp`.
