Use `reads` for both, because Redis and PostgreSQL are data stores here. Use `calls` for synchronous service-to-service or API-to-API interactions, not datastore access. A short example is:
retrievalService -[reads]-> redis 'Checks cache' {
  technology 'Redis'
}
retrievalService -[reads]-> postgres 'Loads data on miss' {
  technology 'PostgreSQL'
}
