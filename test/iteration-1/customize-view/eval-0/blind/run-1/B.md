view c2_containers of mySystem {
  include user
  include mySystem.webapp
  include mySystem.api
  include mySystem.database
  include emailService

  autoLayout lr

  mySystem.webapp {
    navigateTo c2_webapp_details
  }
}
