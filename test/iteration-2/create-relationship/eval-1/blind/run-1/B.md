Short answer: **No, not by default.**

Model only real interactions:

- `uploadService -[async]-> jobQueue "Publishes upload job" { technology "AMQP" }`
- `worker -[reads]-> jobQueue "Consumes job" { technology "AMQP" }`
- `worker -[writes]-> database "Persists result" { technology "PostgreSQL" }`

Add a return relationship from `worker` back to `uploadService` **only if** there is an actual callback/command/notification path (for example, worker calls upload service webhook).
