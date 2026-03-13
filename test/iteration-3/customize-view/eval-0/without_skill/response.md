autoLayout LeftRight

include mySystem.webapp with {
  navigateTo c2_webapp_details
}

rank source { user }
rank sink { mySystem.database, emailService }
