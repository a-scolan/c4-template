Relationship choice: use `reads` for both Redis and PostgreSQL.
Rule: Use `calls` for service behavior, but use `reads` when a service is reading from a cache, database, or directory.
Example:
retrievalService -[reads]-> redisCache 'Checks cache'
retrievalService -[reads]-> primaryDatabase 'Fetches on cache miss'
Anti-pattern:
retrievalService -[calls]-> primaryDatabase 'Fetch data'
