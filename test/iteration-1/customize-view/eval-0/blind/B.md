view c2_containers {
  include mySystem.webapp with {
    navigateTo c2_webapp_details
  }

  rank source { user }
  rank sink { mySystem.database, emailService }
  autoLayout LeftRight
}
