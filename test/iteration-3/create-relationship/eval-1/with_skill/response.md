Relationship choice: `async` for the queue flow, then `writes` for persistence.
Short rule: Keep the async path one-way: producer -> queue -> worker -> database. Do not add a return relationship from `worker` back to `uploadService` just to imply completion or ACK.
Minimal example:
uploadService -[async]-> jobQueue 'Publishes job' {
  technology 'AMQP'
}
jobQueue -[async]-> worker 'Delivers job' {
  technology 'AMQP'
}
worker -[writes]-> primaryDatabase 'Stores processing result' {
  technology 'PostgreSQL'
}
Counter-example / anti-pattern:
worker -[calls]-> uploadService 'Send completion'
That invents a callback path the model does not need. If retry or callback timing matters, move that story to `create-sequence-view`.
