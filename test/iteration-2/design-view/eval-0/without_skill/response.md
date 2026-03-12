Place this in your project view file, for example `projects/template/system-views.c4`, inside `views 'C2'` rather than at the root level.

```likec4
views 'C2' {
  view c2_containers {
    title 'Containers'
    description 'C2 view with the parent system, its containers, the user, and neighboring email service'

    include user
    include mySystem
    include mySystem.*
    include emailService

    include mySystem.webapp with {
      navigateTo c2_webapp_detail
    }

    rank source { user }
    rank sink { mySystem.database, emailService }
  }

  view c2_webapp_detail {
    title 'Web Application Detail'

    include user
    include mySystem
    include mySystem.webapp
    include mySystem.api
    include emailService

    rank source { user }
    rank sink { mySystem.api, emailService }
  }
}
```

This keeps the view in the correct `C2` folder, explicitly shows the parent system, focuses on its child containers, keeps the neighboring context visible, and adds the drill-down from `mySystem.webapp` with `navigateTo`.