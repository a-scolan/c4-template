Pattern: **Async queue/worker processing**.

Use a queue as the handoff boundary between producer API and consumer worker.

```likec4
jobQueue = Container_Queue 'Job Queue' {
  technology 'RabbitMQ'
  description 'Asynchronous job buffer.'
}

api -[async]-> jobQueue 'Publishes job' {
  technology 'AMQP'
}

worker -[async]-> jobQueue 'Consumes job' {
  technology 'AMQP'
}
```

Critical mistake to avoid:
- Don’t draw a direct synchronous `worker -> api` return to represent completion; that breaks the async intent.

Substitutions:
- `parent`: align queue/worker placement with your existing model structure.
- `exact kinds`: map to workspace-defined queue and async relationship taxonomy.
- `names` + `tech`: use real service names, broker, and protocol.