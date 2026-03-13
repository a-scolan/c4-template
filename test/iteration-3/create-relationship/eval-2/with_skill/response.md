Relationship choice: use `reads` for Redis and PostgreSQL.
Short rule: Reserve `-[calls]->` for service-to-service behavior. Use `-[reads]->` for data access, and `-[writes]->` when the service persists or mutates data.
Minimal example:
retrievalService -[reads]-> redisCache 'Checks cache' {
  technology 'Redis'
}
retrievalService -[reads]-> primaryDatabase 'Fetches on cache miss' {
  technology 'PostgreSQL'
}
If it also refreshes cache:
retrievalService -[writes]-> redisCache 'Refreshes cached value'
Counter-example / anti-pattern:
retrievalService -[calls]-> primaryDatabase 'Fetch data'
That is weaker and misleading here because a database read is data access, not a service invocation.
