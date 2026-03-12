Use `reads` for both Redis and PostgreSQL here.

Rule:
- Use `-[calls]->` for service-to-service interactions
- Use `-[reads]->` when a service fetches data from a cache, database, or store
- Use `-[writes]->` when a service persists or mutates data

Short example:

```likec4
retrievalService -[reads]-> redisCache 'Checks cache'
retrievalService -[reads]-> postgresDb 'Loads fallback data'
```

If `retrievalService` was invoking another application service, that would be `-[calls]->` instead.