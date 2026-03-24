Pattern: Async queue/worker.

Minimal scaffold:
queue = Container_Queue 'Job Queue' {
  technology 'RabbitMQ'
  description 'Buffers asynchronous work.'
}

api -[async]-> queue 'Publishes job' {
  technology 'AMQP'
}

worker -[async]-> queue 'Consumes job' {
  technology 'AMQP'
}

Mistake to avoid:
- Do not add a synchronous return call from `worker` back to `api`; async flows are one-way.

Substitute before finalizing:
- parent: place `queue` and `worker` under the correct system/container boundary
- exact kinds: swap `Container_Queue`, `Container`, or `async` for the exact declared workspace kinds and relationship types
- names: use your real queue and worker names
- tech: keep `RabbitMQ` on the queue and `AMQP` on the arrows
