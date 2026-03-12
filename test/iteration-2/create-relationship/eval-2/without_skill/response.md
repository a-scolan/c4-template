Use `-[reads]->` for Redis and PostgreSQL here.

Rule of thumb:
- Use `-[calls]->` for **service-to-service** interactions
- Use `-[reads]->` for **data access when reading**
- Use `-[writes]->` for **data access when mutating or persisting**

Short example:

```likec4
retrievalService -[reads]-> redis 'Checks cache' {
  technology 'Redis'
}

retrievalService -[reads]-> postgres 'Loads records' {
  technology 'PostgreSQL'
}
```

If the service later updates state, then use `-[writes]->`, for example:

```likec4
retrievalService -[writes]-> redis 'Warms cache' {
  technology 'Redis'
}
```

So in your case: **Redis read = `reads`, PostgreSQL read = `reads`, service API call = `calls`.**