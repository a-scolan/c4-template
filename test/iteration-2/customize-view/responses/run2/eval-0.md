view c2 {
  autoLayout leftRight
  include user, webapp, database, mailService
  user -> webapp
  webapp -> database
  webapp -> mailService
  webapp -> webapp-detail
}