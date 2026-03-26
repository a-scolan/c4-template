Use a **C2 folder** and keep parent + focus + neighbors explicit.

```likec4
views 'C2' {
  view c2_corePlatform {
    title 'Core Platform - Container View'

    // Parent boundary + actor + external dependency
    include customer
    include corePlatform
    include externalEmailService

    // Focus internals (containers)
    include corePlatform.*

    // Neighbors (incoming + outgoing around the focus)
    include -> corePlatform
    include corePlatform ->

    // Drill-down from the web app to a C3 detail
    include corePlatform.webApplication with {
      navigateTo c3_webApplication
    }
  }
}
```

This placement and include strategy matches a proper C2: system boundary visible, containers visible, user/external system visible, and navigation wired from the web application.