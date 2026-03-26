For a clean C2 (Container) setup with drill-down from the web application, model both a context view and a container view.

Recommended LikeC4 skeleton in `projects/template/`:

- Define participants in the model:
  - `person user`
  - `system mySystem`
  - `system externalEmailService`
- Define containers in `mySystem`:
  - `container webApp`
  - `container api`
  - `container db`
- Define relationships:
  - `user -> mySystem.webApp`
  - `mySystem.webApp -> mySystem.api`
  - `mySystem.api -> mySystem.db`
  - `mySystem.api -> externalEmailService`
- Add views:
  - C1/context: include `user`, `mySystem`, `externalEmailService`
  - C2/container: include `mySystem.*` and `externalEmailService`
  - Drill-down view: focus on `mySystem.webApp` and its direct collaborators

This keeps the C2 explicit and provides clear drill-down from the web application.For a clean C2 (Container) setup with drill-down from the web application, model both context and container views.

Recommended LikeC4 skeleton (place in your project model files under `projects/template/`):

- Define actors/systems in context model:
  - `person user`
  - `system mySystem`
  - `system externalEmailService`
- Define containers inside `mySystem`:
  - `container webApp`
  - `container api`
  - `container db`
- Define relationships:
  - `user -> mySystem.webApp`
  - `mySystem.webApp -> mySystem.api`
  - `mySystem.api -> mySystem.db`
  - `mySystem.api -> externalEmailService`
- Add views:
  - C1/context view including `user`, `mySystem`, `externalEmailService`
  - C2/container view for `mySystem.*` and `externalEmailService`
  - Drill-down element view scoped to `mySystem.webApp` (showing immediate collaborators)

This gives the exact C2 coverage you asked for and keeps drill-down navigation explicit from the web application.Use a **two-view element model**: one **System Landscape (C1-ish)** and one **Container (C2)** focused on drill-down from the web app.

Recommended skeleton placement in this workspace:
- Model: `template/system-model.c4`-style split (context + containers)
- Views: `template/system-views.c4`-style split (landscape + container)

LikeC4 skeleton:

```likec4
specification {
  element person
  element system
  element container
}

model {
  user = person "User"

  mySystem = system "My System" {
    webapp = container "Web Application" "Handles UI and upload flow"
    api = container "API Service"
    db = container "Database"
  }

  emailSvc = system "External Email Service"

  user -> mySystem.webapp "Uses"
  mySystem.webapp -> mySystem.api "Calls"
  mySystem.api -> mySystem.db "Reads/Writes"
  mySystem.api -> emailSvc "Sends notifications"
}

views {
  view landscape of mySystem {
    include user
    include mySystem
    include emailSvc
    title "System Landscape"
  }

  view containers of mySystem {
    include *
    include user
    include emailSvc
    title "C2 - Containers"
    description "Container view with drill-down anchored on Web Application"
  }

  view webapp_drilldown of mySystem.webapp {
    include *
    title "Web Application Drill-down"
  }
}
```

Why this is clean:
- Shows **user + system + external email service** in the landscape.
- Shows **system internals (containers)** in C2.
- Provides explicit **drill-down from `webapp`**.