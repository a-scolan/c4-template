view c2_containers {
  title 'Containers'

  autoLayout LeftRight

  include user
  include mySystem.*
  include mySystem.webapp with {
    navigateTo c2_webapp_details
  }
  include emailService

  rank source { user }
  rank sink { mySystem.database, emailService }
}