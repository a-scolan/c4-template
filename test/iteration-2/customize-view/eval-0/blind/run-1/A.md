view c2_containers {
  autoLayout LeftRight
  include *
  include user -> *
  include * -> database
  include * -> mailService

  user -> webapp
  webapp -> database
  webapp -> mailService

  webapp {
    navigateTo c3_webapp
  }
}
