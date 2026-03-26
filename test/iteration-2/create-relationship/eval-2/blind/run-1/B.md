# Eval 2 — retrievalService reads Redis then PostgreSQL: calls or reads?

## 1. Relationship choice

Use **`reads`** for both.

## 2. Rule

Use `reads` for any data access — cache lookup, database query, directory read. Reserve `calls` for service-to-service behavior where one service invokes another service's logic. Databases and caches are not "called"; they are "read from" or "written to".

## 3. Minimal example

```likec4
retrievalService -[reads]-> redisCache 'Checks cache'
retrievalService -[reads]-> primaryDatabase 'Fetches on cache miss'
```

## 4. Anti-pattern

```likec4
// ❌ Wrong: databases and caches are not generic service calls
retrievalService -[calls]-> primaryDatabase 'Fetch data'
retrievalService -[calls]-> redisCache 'Get value'
```
