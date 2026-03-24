Put it in `system-views.c4` under `views 'C2'`. The clean include strategy is: actor + external system, then the parent system, then its direct containers, and add drill-down on the web application.

```likec4
views 'C2' {
  view c2_corePlatform {
    title 'Core Platform - Containers'
    description 'System boundary, containers, user, and email integration'

    include user
    include externalEmailService

    include corePlatform
    include corePlatform.*

    include corePlatform.webApp with {
      navigateTo c3_webApp
    }
  }
}
```

If you want the full neighbor context later, add directed includes such as `include -> corePlatform.*` and `include corePlatform.* ->`, but the skeleton above is the right starting shape and the right category.
