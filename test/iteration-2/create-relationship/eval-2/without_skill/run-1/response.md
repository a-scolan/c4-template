Use the relationship verb based on **interaction semantics**:

- `calls` = synchronous service/API invocation
- `reads` = read access to a data store
- `writes` = write/update to a data store
- `async` = asynchronous publish/send (queue/topic/event)

For your case (`retrievalService` reading Redis, then PostgreSQL), use **`reads`** for both:

`retrievalService -[reads]-> redis "Lookup cache" { technology "REDIS" }`

`retrievalService -[reads]-> postgres "Fallback query" { technology "PostgreSQL" }`
