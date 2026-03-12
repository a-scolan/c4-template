Use `-[reads]->` for Redis and PostgreSQL because they are data stores. Reserve `-[calls]->` for service-to-service request/response interactions, and use `-[writes]->` when the service persists or mutates data.

```likec4
retrievalService -[reads]-> redisCache 'Check cache'
retrievalService -[reads]-> postgres 'Load record'
retrievalService -[writes]-> auditStore 'Persist access log'
```

Rule of thumb:
- `-[calls]->`: service-to-service interaction
- `-[reads]->`: query or fetch from a cache or database
- `-[writes]->`: persist or update data
