view c2_containers {
  include *

  webapp {
    navigateTo c3_webapp
    link 'Internal spec docs' 'https://intranet.example.local/architecture/specs'
  }
}
