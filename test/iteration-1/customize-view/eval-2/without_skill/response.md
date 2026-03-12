view c2_containers {
  include mySystem.webapp with {
    navigateTo c2_webapp_details
    link https://intranet.example.com/specs/webapp 'Internal spec docs'
  }
}