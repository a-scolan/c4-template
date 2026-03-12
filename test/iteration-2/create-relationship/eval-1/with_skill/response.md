Use `async` for the queue interactions and keep the flow one-way:

```likec4
uploadService -[async]-> jobQueue 'Publishes job' {
  technology 'AMQP'
}

worker -[async]-> jobQueue 'Consumes job' {
  technology 'AMQP'
}

worker -[writes]-> database 'Stores result' {
  technology 'PostgreSQL'
}
```

No, you should **not** draw a return relationship from `worker` back to `uploadService`. That would fake a synchronous callback/ACK path in an async flow. Keep the queue pattern explicit and one-way, and use `-[writes]->` for persistence instead of a generic `calls` relationship.
