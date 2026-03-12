```likec4
view c2_containers {
  autoLayout LeftRight

  include user
  include mySystem.*
  include mySystem.webapp with {
    navigateTo c2_webapp_details
  }
  include emailService

  rank source { user }
}
```