Pattern to apply: **Async queue/worker flow**.

```likec4
queue = Container_Queue 'Job Queue' {
  technology 'RabbitMQ'
  description 'Queue for background jobs.'
}

api -[async]-> queue 'Publishes job' {
  technology 'AMQP'
}

worker -[async]-> queue 'Consumes job' {
  technology 'AMQP'
}
```

Mistake to avoid:
- Don’t add a synchronous response path from `worker` back to `api` as if it were request/response. In this pattern, completion is asynchronous.

Substitutions:
- Replace placeholder element names and kinds with declared workspace types.
- Keep queue and worker under correct parent containers/systems.
- Align technology labels with actual broker/protocol.