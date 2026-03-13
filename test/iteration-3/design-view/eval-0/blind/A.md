Put it in `views 'C2'`, following the workspace convention that non-index views live inside named category folders and typically use `c2_` identifiers. A clean skeleton is:

views 'C2' {
  view c2_containers {
    title 'Containers'
    include user
    include mySystem
    include mySystem.*
    include emailService
    include mySystem.webapp with {
      navigateTo c2_webapp_details
    }
  }

  view c2_webapp_details {
    title 'Web Application Detail'
    include mySystem
    include mySystem.webapp
    include -> mySystem.webapp
    include mySystem.webapp ->
  }
}

Why this shape: the parent system is explicit, the child containers are shown under it, the neighboring context is present (`user`, `emailService`), and the web application has the drill-down hook.
