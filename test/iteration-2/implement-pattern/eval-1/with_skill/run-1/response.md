Pattern: **Async queue/worker**.

Model a queue between producer and consumer, with one-way async relationships.

```likec4
jobQueue = Container_Queue 'Job Queue' {
  technology 'RabbitMQ'
  description 'Buffers background jobs.'
}

api -[async]-> jobQueue 'Publishes job' {
  technology 'AMQP'
}

worker -[async]-> jobQueue 'Consumes job' {
  technology 'AMQP'
}
```

Mistake to avoid:
- Do **not** add a synchronous return call from `worker` to `api` to represent completion. Async flow is one-way in the structural model.

Substitutions:
- `parent`: place `jobQueue` under your actual platform/system parent.
- `exact kinds`: use your declared queue/container kind and async relationship kind.
- `names`: replace `api`, `worker`, `jobQueue` with project names.
- `tech`: keep RabbitMQ/AMQP if accurate, otherwise set real broker/protocol.