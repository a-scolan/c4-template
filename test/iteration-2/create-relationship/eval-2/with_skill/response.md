Use `-[reads]->` for Redis and PostgreSQL, because those are data-access relationships.

Rule of thumb:
- Use `-[calls]->` for service-to-service interactions.
- Use `-[reads]->` when a service retrieves data from a store.
- Use `-[writes]->` when a service mutates or persists data.

Short example:

```likec4
retrievalService -[reads]-> redis 'Checks cache'
retrievalService -[reads]-> postgres 'Fetches records'
```

If `retrievalService` were calling another API or internal service, that would be the case for `-[calls]->` instead.
