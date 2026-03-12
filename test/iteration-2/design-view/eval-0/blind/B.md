Place this in your project `system-views.c4` (the template example is `projects/template/system-views.c4`), inside `views 'C2'`.

```likec4
views 'C2' {
  view c2_containers {
    title 'Containers'

    include user                        // neighbor: initiating actor
    include mySystem                    // parent context
    include mySystem.*                  // focus: all containers
    include emailService                // neighbor: external dependency

    include -> mySystem.*               // incoming neighbors
    include mySystem.* ->               // outgoing neighbors

    include mySystem.webapp with {
      navigateTo c3_webapp
    }
  }
}

views 'C3' {
  view c3_webapp {
    title 'Web Application'

    include mySystem.webapp             // parent container for the C3 scope
    include mySystem.webapp.*           // web application components
    include -> mySystem.webapp          // who calls into the web app
    include mySystem.webapp ->          // what the web app depends on
  }
}
```

Why this is the right skeleton:
- The container view lives under `views 'C2'`, not at the root.
- It keeps the parent system visible with `include mySystem`.
- It focuses on the child containers with `include mySystem.*`.
- It preserves neighbor context with `user`, `emailService`, plus incoming/outgoing relationship includes.
- The drill-down is attached to `mySystem.webapp`, which is the natural next detail level.

I would start without layout hints and only add `autoLayout` or a small `rank` hint later if the rendered view is genuinely hard to read.
