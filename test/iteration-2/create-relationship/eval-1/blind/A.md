For that flow, keep it **one-way and async**. I would model it like this:

```likec4
uploadService -[async]-> jobQueue 'Publishes upload job' {
  technology 'AMQP'
}

jobQueue -[async]-> worker 'Delivers job to worker' {
  technology 'AMQP'
}

worker -[writes]-> database 'Stores upload result' {
  technology 'PostgreSQL'
}
```

You should **not** add a return relationship from `worker` back to `uploadService` unless there is a real, separate callback or notification mechanism.

Why:
- `-[async]->` is the right kind for queue-based messaging
- `-[writes]->` is the right kind for persistence
- An ACK or internal processing completion is **not** usually modeled as a callback relationship

So the clean baseline is: producer -> queue -> consumer -> database. No boomerang arrow.